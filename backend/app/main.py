from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Form, Request
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any, Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, StreamingResponse, JSONResponse
from pydantic import BaseModel
from app.config.settings import settings
from app.utils.logger import logger
from app.services.supabase_service import SupabaseService
from app.services.parser_service import ParserService
from app.services.langgraph_service import LangGraphService
from app.utils.auth import get_current_user
from app.dependencies import get_supabase_client
from app.services.hr_chat_service import HRChatService
from app.services.finance_chat_service import FinanceChatService
from app.services.operations_chat_service import OperationsChatService
from app.services.sales_chat_service import SalesChatService
from app.services.retail_chat_service import RetailChatService

from app.services.pdf_export.operations_pdf_export_service import OperationsPDFExporter
from app.services.pdf_export.hr_pdf_export_service import HRPDFExporter
from app.services.pdf_export.finance_pdf_export_service import FinancePDFExporter
from app.services.pdf_export.sales_pdf_export_service import SalesPDFExporter
from app.services.pdf_export.retail_pdf_export_service import RetailPDFExporter

from supabase import Client
import hmac
import hashlib
import io
import json

app = FastAPI(title="AI Analyst Backend", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

langgraph_service = LangGraphService()

def get_supabase_service(supabase_client: Client = Depends(get_supabase_client)) -> SupabaseService:
    return SupabaseService(supabase_client)

class ChatRequest(BaseModel):
    file_id: str
    question: str

class AnalyzeRequest(BaseModel):
    spreadsheet_type: str

class SubscriptionResponse(BaseModel):
    id: str
    user_id: str
    plan: str
    status: str
    credits: int
    total_credits: int
    credits_left: int
    started_at: str
    expires_at: str | None

class ExportPDFRequest(BaseModel):
    file_id: Optional[str] = None
    insights: Optional[Dict] = None

# Dictionary to map spreadsheet types to PDF exporters and analysis services
PDF_EXPORTERS = {
    "finance": FinancePDFExporter(),
    "hr": HRPDFExporter(),
    "operations": OperationsPDFExporter(),
    "sales": SalesPDFExporter(),
    "retail": RetailPDFExporter(),
}

CHAT_SERVICES = {
    "finance": FinanceChatService(),
    "hr": HRChatService(),
    "operations": OperationsChatService(),
    "sales": SalesChatService(),
    "retail": RetailChatService(),
}

def verify_flutterwave_signature(payload: bytes, signature: str) -> bool:
    """
    Verify Flutterwave webhook signature using your secret hash.
    """
    computed_hash = hmac.new(
        settings.flw_secret_hash.encode("utf-8"),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(computed_hash, signature)


@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    spreadsheet_type: str = Form(...),
    user_id: str = Depends(get_current_user),
    supabase_service: SupabaseService = Depends(get_supabase_service)
):
    try:
        # Validate file type
        file_ext = file.filename.split(".")[-1].lower()
        allowed_types = settings.allowed_file_types.split(",")
        if file_ext not in allowed_types:
            raise HTTPException(status_code=400, detail=f"Invalid file type. Allowed: {allowed_types}")

        # Validate spreadsheet type
        allowed_spreadsheet_types = ["Retail", "HR", "Sales", "Finance", "Operations"]
        if spreadsheet_type not in allowed_spreadsheet_types:
            raise HTTPException(status_code=400, detail=f"Invalid spreadsheet type. Allowed: {allowed_spreadsheet_types}")

        # Validate file size
        file_content = await file.read()
        if len(file_content) > settings.max_file_size:
            raise HTTPException(status_code=400, detail="File size exceeds limit")

        # Upload to Supabase
        file_path = await supabase_service.upload_file(file_content, file.filename, user_id)

        # Save file metadata
        result = await supabase_service.save_file_metadata(
            file_name=file.filename,
            file_path=file_path,
            user_id=user_id,
            file_size=len(file_content),
            file_type=file_ext,
            spreadsheet_type=spreadsheet_type
        )

        logger.info(
            "File processed successfully",
            file_name=file.filename,
            user_id=user_id,
            spreadsheet_type=spreadsheet_type
        )
        return {"file_path": file_path, "file_id": result[0]["id"]}
    except Exception as e:
        logger.error(
            "Error processing file",
            error=str(e),
            file_name=file.filename,
            spreadsheet_type=spreadsheet_type
        )
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/files")
async def list_files(
    user_id: str = Depends(get_current_user),
    supabase_service: SupabaseService = Depends(get_supabase_service)
):
    try:
        files = await supabase_service.list_user_files(user_id)
        return {"files": files}
    except Exception as e:
        logger.error("Error listing files", error=str(e), user_id=user_id)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/files/{file_id}")
async def get_file(
    file_id: str,
    user_id: str = Depends(get_current_user),
    supabase_service: SupabaseService = Depends(get_supabase_service)
):
    try:
        file = await supabase_service.get_file_by_id(file_id, user_id)
        return file
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error("Error retrieving file", error=str(e), file_id=file_id, user_id=user_id)
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/full-analyze/{file_id}")
async def full_analyze_file(
    file_id: str,
    request: AnalyzeRequest,
    user_id: str = Depends(get_current_user),
    supabase_service: SupabaseService = Depends(get_supabase_service)
):
    try:
        # Get file metadata
        file = await supabase_service.get_file_by_id(file_id, user_id)
        if file["status"] in ["processing", "fully_analyzed"]:
            raise HTTPException(status_code=400, detail=f"File is already {file['status']}")

        # Validate spreadsheet_type
        if file["spreadsheet_type"] != request.spreadsheet_type:
            raise HTTPException(
                status_code=400,
                detail=f"Spreadsheet type mismatch: expected {file['spreadsheet_type']}, got {request.spreadsheet_type}"
            )

        # Get file size (in bytes) and calculate credits to deduct
        file_size = file.get("file_size", 0)
        if file_size <= 0:
            raise HTTPException(status_code=400, detail="Invalid file size")

        # Credit deduction: 1 credit per KB for <1MB, 0.5 credits per KB for >=1MB
        if file_size < 1024 * 1024:  # < 1 MB
            credits_to_deduct = max(100, int(file_size / 1024))
        else:  # >= 1 MB
            credits_to_deduct = max(1000, int(file_size / 1024 / 2))
        logger.info("Calculated credits to deduct", file_id=file_id, file_size=file_size, credits=credits_to_deduct)

        # Update status to processing
        await supabase_service.update_file_status(file_id, user_id, "processing")

        # Fetch user subscription
        subscription_response = supabase_service.client.table('subscriptions').select('*').eq('user_id', user_id).single().execute()
        if not subscription_response.data:
            raise HTTPException(status_code=403, detail="No subscription found")
        subscription = subscription_response.data
        plan = subscription['plan']
        credits_left = subscription['credits_left']

        # Initialize ParserService
        parser_service = ParserService(supabase_service.client)
        # Parse spreadsheet with computed insights
        json_data, description, computed_insights = await parser_service.parse_spreadsheet(
            file["file_path"], file["file_type"], file["spreadsheet_type"], compute_insights=True
        )

        # Validate json_data
        if not isinstance(json_data, (dict, list)) or not json_data:
            raise HTTPException(status_code=400, detail="Invalid or empty JSON data")

        ai_insights = None
        if plan in ['plus', 'pro']:
            if credits_left < credits_to_deduct:
                raise HTTPException(status_code=402, detail=f"Insufficient credits: need {credits_to_deduct}, have {credits_left}")

            ai_insights = await langgraph_service.generate_insights(json_data, description)

            # Deduct credits atomically from credits_left
            new_credits_left = credits_left - credits_to_deduct
            update_response = supabase_service.client.table('subscriptions').update({
                'credits_left': new_credits_left
            }).eq('user_id', user_id).execute()
            if not update_response.data:
                raise HTTPException(status_code=500, detail="Failed to update subscription credits")
            logger.info("Credits deducted", user_id=user_id, file_id=file_id, deducted=credits_to_deduct, remaining=new_credits_left)

        # Save analysis results
        analysis_result = await supabase_service.save_analysis_result(
            file_id, user_id, json_data, description, computed_insights, ai_insights
        )

        # Update file status to fully_analyzed
        await supabase_service.update_file_status(file_id, user_id, "fully_analyzed")

        logger.info(
            "Full analysis completed",
            file_id=file_id,
            user_id=user_id,
            spreadsheet_type=request.spreadsheet_type,
            sheets=list(json_data.keys()),
            ai_enabled=bool(ai_insights),
            credits_deducted=credits_to_deduct if ai_insights else 0
        )
        return {
            "file_id": file_id,
            "analysis_id": analysis_result[0]["id"],
            "status": "fully_analyzed",
            "sheets": list(json_data.keys())
        }
    except HTTPException as e:
        await supabase_service.update_file_status(file_id, user_id, "error")
        raise e
    except Exception as e:
        await supabase_service.update_file_status(file_id, user_id, "error")
        logger.error(
            "Error in full analysis",
            error=str(e),
            file_id=file_id,
            user_id=user_id,
            spreadsheet_type=request.spreadsheet_type
        )
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ai-analyze/{file_id}")
async def ai_analyze_file(
    file_id: str,
    request: AnalyzeRequest,
    user_id: str = Depends(get_current_user),
    supabase_service: SupabaseService = Depends(get_supabase_service)
):
    try:
        subscription = await supabase_service.get_subscription_by_user_id(user_id)
        if not subscription or subscription["status"] != "active" or subscription["plan"] == "free":
            raise HTTPException(status_code=403, detail="Active subscriptions required to analyze with AI.")
        
        # Get file metadata
        file = await supabase_service.get_file_by_id(file_id, user_id)
        if file["status"] != "fully_analyzed":
            raise HTTPException(status_code=400, detail="File must be fully analyzed with manual analysis first")

        # Validate spreadsheet_type
        if file["spreadsheet_type"] != request.spreadsheet_type:
            raise HTTPException(
                status_code=400,
                detail=f"Spreadsheet type mismatch: expected {file['spreadsheet_type']}, got {request.spreadsheet_type}"
            )

        # Get file size (in bytes) and calculate credits to deduct
        file_size = file.get("file_size", 0)
        if file_size <= 0:
            raise HTTPException(status_code=400, detail="Invalid file size")

        # Credit deduction: same as /full-analyze/{file_id}
        if file_size < 1024 * 1024:  # < 1 MB
            credits_to_deduct = max(100, int(file_size / 1024))
        else:  # >= 1 MB
            credits_to_deduct = max(1000, int(file_size / 1024 / 2))
        logger.info("Calculated credits to deduct", file_id=file_id, file_size=file_size, credits=credits_to_deduct)

        # Fetch user subscription
        subscription_response = supabase_service.client.table('subscriptions').select('*').eq('user_id', user_id).single().execute()
        if not subscription_response.data:
            raise HTTPException(status_code=403, detail="No subscription found")
        subscription = subscription_response.data
        plan = subscription['plan']
        credits_left = subscription['credits_left']

        # Check if user is paid
        if plan not in ['plus', 'pro']:
            raise HTTPException(status_code=403, detail="AI analysis requires a Plus or Pro subscription")

        # Check credits
        if credits_left < credits_to_deduct:
            raise HTTPException(status_code=402, detail=f"Insufficient credits: need {credits_to_deduct}, have {credits_left}")

        # Retrieve existing analysis results
        analysis_response = supabase_service.client.table('analysis_results').select('*').eq('file_id', file_id).eq('user_id', user_id).single().execute()
        if not analysis_response.data:
            raise HTTPException(status_code=404, detail="No analysis results found for this file")

        json_data = analysis_response.data['json_data']
        description = analysis_response.data['description']
        computed_insights = analysis_response.data['computed_insights']

        # Validate json_data
        if not isinstance(json_data, (dict, list)) or not json_data:
            raise HTTPException(status_code=400, detail="Invalid or empty JSON data")

        # Run AI analysis
        ai_insights = await langgraph_service.generate_insights(json_data, description)

        # Deduct credits atomically
        new_credits_left = credits_left - credits_to_deduct
        update_response = supabase_service.client.table('subscriptions').update({
            'credits_left': new_credits_left
        }).eq('user_id', user_id).execute()
        if not update_response.data:
            raise HTTPException(status_code=500, detail="Failed to update subscription credits")
        logger.info("Credits deducted", user_id=user_id, file_id=file_id, deducted=credits_to_deduct, remaining=new_credits_left)

        # Update analysis results with AI insights
        update_analysis_response = supabase_service.client.table('analysis_results').update({
            'ai_insights': ai_insights
        }).eq('file_id', file_id).eq('user_id', user_id).execute()
        if not update_analysis_response.data:
            raise HTTPException(status_code=500, detail="Failed to update AI analysis results")

        logger.info(
            "AI analysis completed",
            file_id=file_id,
            user_id=user_id,
            spreadsheet_type=request.spreadsheet_type,
            sheets=list(json_data.keys()),
            credits_deducted=credits_to_deduct
        )
        return {
            "file_id": file_id,
            "analysis_id": analysis_response.data['id'],
            "status": "fully_analyzed",
            "sheets": list(json_data.keys())
        }
    except HTTPException as e:
        logger.error(
            "Error in AI analysis",
            error=str(e),
            file_id=file_id,
            user_id=user_id,
            spreadsheet_type=request.spreadsheet_type
        )
        raise e
    except Exception as e:
        logger.error(
            "Error in AI analysis",
            error=str(e),
            file_id=file_id,
            user_id=user_id,
            spreadsheet_type=request.spreadsheet_type
        )
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analysis/{file_id}")
async def get_analysis(
    file_id: str,
    user_id: str = Depends(get_current_user),
    supabase_service: SupabaseService = Depends(get_supabase_service)
):
    try:
        analysis = await supabase_service.get_analysis_by_file_id(file_id, user_id)
        return analysis
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error("Error retrieving analysis", error=str(e), file_id=file_id, user_id=user_id)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/webhook/flutterwave")
async def flutterwave_webhook(
    request: Request,
    supabase_client: Client = Depends(get_supabase_client)
):
    payload = await request.body()
    headers = dict(request.headers)

    # 🔍 Log raw body once for debugging (remove/obfuscate in production if sensitive)
    body_text = payload.decode("utf-8")
    logger.info("RAW WEBHOOK BODY", extra={"body": body_text})

    # ✅ Validate Flutterwave signature
    signature = headers.get("verif-hash")
    if not signature:
        logger.error("Missing Flutterwave signature", extra={"headers": headers})
        return JSONResponse({"status": "ignored"}, status_code=400)

    if signature != settings.flw_secret_hash:
        logger.error("Invalid Flutterwave signature", extra={"received": signature})
        return JSONResponse({"status": "invalid_signature"}, status_code=400)

    try:
        event = json.loads(body_text)
        data = event.get("data", {})

        # ✅ Only process successful payments
        if data.get("status") != "successful":
            logger.info("Ignoring non-successful payment", extra={"status": data.get("status")})
            return {"status": "ignored"}

        tx_ref = data.get("tx_ref", "")
        tx_id = data.get("id")

        # ✅ Safe parsing of tx_ref (format: sub_userid_plan_timestamp)
        user_id, plan = None, None
        parts = tx_ref.split("_")
        if len(parts) >= 3:
            user_id = parts[1]
            plan = parts[2]

        # ✅ Fallback: use meta if tx_ref not in expected format
        meta = data.get("meta", {})
        if not user_id:
            user_id = meta.get("user_id")
        if not plan:
            plan = meta.get("plan")

        # ✅ Normalize plan to lowercase
        plan = plan.lower() if plan else None

        if not user_id or plan not in ["plus", "pro"]:
            logger.warning("Invalid metadata in webhook", extra={"user_id": user_id, "plan": plan, "tx_ref": tx_ref})
            return JSONResponse({"status": "invalid_metadata"}, status_code=400)

        # ✅ Plan credits
        total_credits = 50000 if plan == "plus" else 100000
        now = datetime.now(timezone.utc)
        expires = now + timedelta(days=30)

        # ✅ Idempotency: check if transaction already exists
        existing_tx = supabase_client.table("transactions").select("id").eq("id", tx_id).execute()
        if existing_tx.data:
            logger.info("Duplicate transaction ignored", extra={"tx_id": tx_id})
            return {"status": "duplicate"}

        # ✅ Record the transaction
        supabase_client.table("transactions").insert({
            "id": tx_id,
            "user_id": user_id,
            "plan": plan,
            "status": "successful",
            "amount": data.get("amount"),
            "currency": data.get("currency"),
            "created_at": now.isoformat()
        }).execute()

        # ✅ Update or insert subscription
        existing_sub = supabase_client.table("subscriptions").select("id").eq("user_id", user_id).execute()
        if existing_sub.data:
            supabase_client.table("subscriptions").update({
                "plan": plan,
                "status": "active",
                "credits": total_credits,
                "total_credits": total_credits,
                "credits_left": total_credits,
                "started_at": now.isoformat(),
                "expires_at": expires.isoformat()
            }).eq("user_id", user_id).execute()
        else:
            supabase_client.table("subscriptions").insert({
                "user_id": user_id,
                "plan": plan,
                "status": "active",
                "credits": total_credits,
                "total_credits": total_credits,
                "credits_left": total_credits,
                "started_at": now.isoformat(),
                "expires_at": expires.isoformat()
            }).execute()

        logger.info("Subscription updated/created", extra={"user_id": user_id, "plan": plan, "tx_id": tx_id})
        return {"status": "success"}

    except json.JSONDecodeError:
        logger.error("Invalid webhook payload format")
        return JSONResponse({"status": "invalid_payload"}, status_code=400)

    except Exception as e:
        # ✅ Always return 200 to avoid Flutterwave retries, but log error
        logger.error("Webhook processing failed", extra={"error": str(e)})
        return {"status": "error_logged"}

@app.get("/subscription", response_model=SubscriptionResponse)
def get_subscription(
    user_id: str = Depends(get_current_user),
    supabase_client: Client = Depends(get_supabase_client)
):
    try:
        response = supabase_client.table('subscriptions').select('*').eq('user_id', user_id).execute()
        subscription = response.data[0] if response.data else None

        if not subscription:
            logger.info("No subscription found, returning default", user_id=user_id)
            return SubscriptionResponse(
                id="",
                user_id=user_id,
                plan="free",
                status="inactive",
                credits=0,
                total_credits=0,
                credits_left=0,
                started_at="",
                expires_at=None
            )

        logger.info("Retrieved subscription details", user_id=user_id, plan=subscription['plan'], credits=subscription['credits'])
        return SubscriptionResponse(
            id=str(subscription['id']),
            user_id=str(subscription['user_id']),
            plan=subscription['plan'],
            status=subscription['status'],
            credits=subscription['credits'],
            total_credits=subscription['total_credits'],
            credits_left=subscription['credits_left'],
            started_at=subscription['started_at'],
            expires_at=subscription['expires_at']
        )
    except Exception as e:
        logger.error("Failed to retrieve subscription", error=str(e), user_id=user_id, response=str(response) if 'response' in locals() else 'no response')
        raise HTTPException(status_code=500, detail=f"Failed to retrieve subscription: {str(e)}")


@app.post("/chat")
async def chat(
    request: ChatRequest,
    user_id: str = Depends(get_current_user),
    supabase_service: SupabaseService = Depends(get_supabase_service)
):
    try:
        # Get file metadata to determine spreadsheet_type
        file = await supabase_service.get_file_by_id(request.file_id, user_id)
        if not file:
            raise HTTPException(status_code=404, detail="File not found")

        spreadsheet_type = file.get("spreadsheet_type", "").lower()
        if not spreadsheet_type:
            raise HTTPException(status_code=400, detail="File has no spreadsheet type")

        # Get chat service based on spreadsheet_type
        chat_service = CHAT_SERVICES.get(spreadsheet_type)
        if not chat_service:
            raise HTTPException(
                status_code=400,
                detail=f"No chat service available for spreadsheet type: {spreadsheet_type}"
            )

        # Get analysis data and raw_data
        analysis = await supabase_service.get_analysis_by_file_id(request.file_id, user_id)
        if not analysis:
            raise HTTPException(status_code=404, detail="Analysis not found for this file")

        # Extract raw_data from analysis (json_data)
        raw_data = analysis.get("json_data")

        if isinstance(raw_data, dict):
            raw_data = [raw_data]

        if isinstance(raw_data, str):
            raw_data = json.loads(raw_data)

        if not isinstance(raw_data, list) or not all(isinstance(item, dict) for item in raw_data):
            logger.error("Invalid raw_data format: expected list of dictionaries", file_id=file_id, user_id=user_id)
            raise HTTPException(status_code=400, detail="Invalid raw_data format: expected list of dictionaries")

        # Get chat history
        chat_history = await supabase_service.get_chat_history(request.file_id, user_id)

        # Generate answer using the appropriate chat service
        answer = await chat_service.process_chat(
            file_id=request.file_id,
            user_id=user_id,
            question=request.question,
            analysis_data=analysis,
            raw_data=raw_data,
            chat_history=chat_history
        )

        # Save chat history
        await supabase_service.save_chat_history(
            file_id=request.file_id,
            analysis_id=analysis["id"],
            user_id=user_id,
            question=request.question,
            answer=answer
        )

        logger.info("Chat response generated", file_id=request.file_id, user_id=user_id, spreadsheet_type=spreadsheet_type)
        return {"file_id": request.file_id, "question": request.question, "answer": answer}
    except HTTPException as e:
        logger.error(
            "Error processing chat",
            error=str(e.detail),
            file_id=request.file_id,
            user_id=user_id,
            spreadsheet_type=spreadsheet_type if 'spreadsheet_type' in locals() else "unknown"
        )
        raise e
    except Exception as e:
        logger.error(
            "Error processing chat",
            error=str(e),
            file_id=request.file_id,
            user_id=user_id,
            spreadsheet_type=spreadsheet_type if 'spreadsheet_type' in locals() else "unknown"
        )
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/chat/history/{file_id}")
async def get_chat_history(
    file_id: str,
    user_id: str = Depends(get_current_user),
    supabase_service: SupabaseService = Depends(get_supabase_service)
):
    try:
        chat_history = await supabase_service.get_chat_history(file_id, user_id)
        logger.info("Chat history retrieved", file_id=file_id, user_id=user_id, message_count=len(chat_history))
        return {"history": chat_history}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error("Error retrieving chat history", error=str(e), file_id=file_id, user_id=user_id)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/export/pdf/{file_id}")
async def export_pdf_report(
    file_id: str,
    request: ExportPDFRequest = None,  # Make optional
    user_id: str = Depends(get_current_user),
    supabase_service: SupabaseService = Depends(get_supabase_service)
):
    """Export analysis insights as a beautifully formatted PDF report"""
    try:
        subscription = await supabase_service.get_subscription_by_user_id(user_id)
        if not subscription or subscription["status"] != "active" or subscription["plan"] == "free":
            raise HTTPException(status_code=403, detail="Active subscription required to export PDFs")

        # Get file metadata
        file = await supabase_service.get_file_by_id(file_id, user_id)
        if not file:
            raise HTTPException(status_code=404, detail="File not found")
        
        # Debug logging
        logger.info("File data retrieved", file_data=file, file_id=file_id, user_id=user_id)
        
        if file["status"] != "fully_analyzed":
            raise HTTPException(status_code=400, detail="File must be fully analyzed before exporting to PDF")

        # Get spreadsheet_type
        spreadsheet_type = file.get("spreadsheet_type", "").lower()
        if not spreadsheet_type:
            raise HTTPException(status_code=400, detail="File has no spreadsheet type")

        # Get PDF exporter based on spreadsheet_type
        exporter = PDF_EXPORTERS.get(spreadsheet_type)
        if not exporter:
            raise HTTPException(
                status_code=400,
                detail=f"No PDF exporter available for spreadsheet type: {spreadsheet_type}"
            )

        # Get analysis data
        analysis = await supabase_service.get_analysis_by_file_id(file_id, user_id)
        if not analysis or not analysis.get("computed_insights"):
            raise HTTPException(status_code=404, detail="No computed insights found for this file")
        
        # Debug logging for analysis
        logger.info("Analysis data retrieved", analysis_keys=list(analysis.keys()) if analysis else [], file_id=file_id)

        # Extract the file name safely with multiple fallbacks
        file_name = (
            file.get("filename") or
            file.get("file_name") or 
            file.get("name") or 
            file.get("original_name") or 
            f"File_{file_id[:8]}"
        )
        
        # Ensure it's a string and not empty
        if not isinstance(file_name, str) or not file_name.strip():
            file_name = f"Analysis_{file_id[:8]}"
            
        logger.info("Final file name determined", file_name=file_name, file_id=file_id)

        # Generate PDF using computed_insights
        pdf_content = exporter.generate_pdf(
            insights = analysis["computed_insights"].get("Sheet1", analysis["computed_insights"])
        )

        # Create filename for download
        safe_filename = "".join(c for c in file_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        if not safe_filename:
            safe_filename = f"Analysis_{file_id[:8]}"
        pdf_filename = f"{safe_filename}_Analysis_Report.pdf"
        
        logger.info("PDF filename created", pdf_filename=pdf_filename, file_id=file_id)

        logger.info("PDF report generated successfully", 
                   file_id=file_id, user_id=user_id, pdf_size=len(pdf_content))

        # Return PDF as downloadable response using StreamingResponse
        return StreamingResponse(
            io.BytesIO(pdf_content),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{pdf_filename}"',  # Add quotes
            }
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error("Error generating PDF report", 
                    error=str(e), file_id=file_id, user_id=user_id)
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF report: {str(e)}")

@app.delete("/files/{file_id}")
async def delete_file(
    file_id: str, 
    user_id: str = Depends(get_current_user),
    supabase_service: SupabaseService = Depends(get_supabase_service)):
    try:
        await supabase_service.delete_file(file_id, user_id)
        logger.info("File deleted successfully", file_id=file_id, user_id=user_id)
        return {"message": "File and associated data deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error("Error deleting file", error=str(e), file_id=file_id, user_id=user_id)
        raise HTTPException(status_code=500, detail=str(e))