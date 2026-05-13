import pandas as pd
import io
import aiohttp
import json
from fastapi import HTTPException
from app.utils.logger import logger
from app.services.sales_analysis_service import SalesAnalysisService
from app.services.retail_analysis_service import RetailAnalysisService
from app.services.hr_analysis_service import HRAnalysisService
from app.services.finance_analysis_service import FinanceAnalysisService
from app.services.operations_analysis_service import OperationsAnalysisService
from supabase import Client

class ParserService:
    def __init__(self, supabase_client: Client):
        self.supabase_client = supabase_client
        self.sales_analysis_service = SalesAnalysisService()
        self.retail_analysis_service = RetailAnalysisService()
        self.hr_analysis_service = HRAnalysisService()
        self.finance_analysis_service = FinanceAnalysisService()
        self.operations_analysis_service = OperationsAnalysisService()

    async def parse_spreadsheet(
        self,
        storage_path: str,            # e.g. "user123/fake_business_data.xlsx"
        file_type: str,               # "csv", "xls", "xlsx"
        spreadsheet_type: str,        # "Sales", "HR", etc.
        compute_insights: bool = True
    ) -> tuple[dict[str, list], dict[str, str], dict[str, dict] | None]:
        try:
            # Split path into folder + filename
            folder = storage_path.rsplit("/", 1)[0] if "/" in storage_path else ""
            file_name = storage_path.rsplit("/", 1)[1] if "/" in storage_path else storage_path

            # Check if file exists in bucket
            objects = self.supabase_client.storage.from_("spreadsheets").list(folder)
            if not any(obj["name"] == file_name for obj in objects):
                raise HTTPException(status_code=404, detail=f"File not found in storage: {storage_path}")

            # Create signed download URL (valid 60s)
            signed_url_response = self.supabase_client.storage.from_("spreadsheets").create_signed_url(storage_path, 60)

            # Debug raw response
            logger.debug("Signed URL raw response", response=signed_url_response)

            download_url = None
            if isinstance(signed_url_response, dict):
                # Handle both cases
                download_url = signed_url_response.get("signedURL") or signed_url_response.get("signed_url")
                if download_url and download_url.startswith("/"):
                    # Prepend Supabase base URL
                    download_url = f"{settings.supabase_url}{download_url}"
            elif isinstance(signed_url_response, str):
                download_url = signed_url_response

            if not download_url:
                raise HTTPException(status_code=500, detail="Failed to generate signed URL")

            # Download file from signed URL
            async with aiohttp.ClientSession() as session:
                async with session.get(download_url) as response:
                    if response.status != 200:
                        error_detail = await response.text()
                        raise HTTPException(
                            status_code=400,
                            detail=f"Failed to download file: {response.reason} - {error_detail}"
                        )
                    file_content = await response.read()

            # Parse into DataFrame(s)
            json_data = {}
            description = {}
            computed_insights = {} if compute_insights else None

            if file_type == "csv":
                # CSV files don't have multiple sheets
                df = pd.read_csv(io.BytesIO(file_content))
                json_data["Sheet1"] = json.loads(df.to_json(orient="records"))
                description["Sheet1"] = self._generate_description(df)
                if compute_insights:
                    computed_insights["Sheet1"] = self._compute_insights(df, spreadsheet_type)
            elif file_type in ["xls", "xlsx"]:
                # Load all sheets for Excel files
                dfs = pd.read_excel(io.BytesIO(file_content), engine="openpyxl", sheet_name=None)
                for sheet_name, df in dfs.items():
                    json_data[sheet_name] = json.loads(df.to_json(orient="records"))
                    description[sheet_name] = self._generate_description(df)
                    if compute_insights:
                        computed_insights[sheet_name] = self._compute_insights(df, spreadsheet_type)
            else:
                raise HTTPException(status_code=400, detail=f"Unsupported file type: {file_type}")

            logger.info(
                "Spreadsheet parsed successfully",
                file_path=storage_path,
                spreadsheet_type=spreadsheet_type,
                sheets=list(json_data.keys()),
                computed_insights=bool(computed_insights)
            )
            return json_data, description, computed_insights

        except HTTPException as e:
            logger.error(
                "Failed to parse spreadsheet",
                error=str(e),
                file_path=storage_path,
                spreadsheet_type=spreadsheet_type,
                error_detail=e.detail
            )
            raise
        except Exception as e:
            logger.error(
                "Failed to parse spreadsheet",
                error=str(e),
                file_path=storage_path,
                spreadsheet_type=spreadsheet_type
            )
            raise HTTPException(status_code=500, detail=f"Parsing error: {str(e)}")

    def _compute_insights(self, df: pd.DataFrame, spreadsheet_type: str) -> dict:
        try:
            if spreadsheet_type == "Sales":
                return self.sales_analysis_service.compute_sales_insights(df)
            elif spreadsheet_type == "Retail":
                return self.retail_analysis_service.compute_retail_insights(df)
            elif spreadsheet_type == "HR":
                return self.hr_analysis_service.compute_hr_insights(df)
            elif spreadsheet_type == "Finance":
                return self.finance_analysis_service.compute_finance_insights(df)
            elif spreadsheet_type == "Operations":
                return self.operations_analysis_service.compute_operations_insights(df)
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid spreadsheet type: {spreadsheet_type}"
                )
        except Exception as e:
            logger.error(
                "Failed to compute insights",
                error=str(e),
                spreadsheet_type=spreadsheet_type
            )
            raise HTTPException(status_code=500, detail=f"Insight computation error: {str(e)}")

    def _generate_description(self, df: pd.DataFrame) -> str:
        try:
            columns = df.columns.tolist()
            dtypes = df.dtypes.to_dict()
            row_count = len(df)
            description = f"The spreadsheet contains {row_count} rows and {len(columns)} columns. "
            description += "Columns and their data types:\n"
            for col, dtype in dtypes.items():
                description += f"- {col}: {dtype}\n"
            
            # Basic summary for numeric columns
            numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
            if numeric_cols.any():
                description += "\nSummary of numeric columns:\n"
                for col in numeric_cols:
                    description += f"- {col}: min={df[col].min():.2f}, max={df[col].max():.2f}, mean={df[col].mean():.2f}\n"
            
            return description
        except Exception as e:
            logger.error("Failed to generate description", error=str(e))
            return "Unable to generate description due to an error."