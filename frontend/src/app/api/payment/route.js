import { NextResponse } from "next/server";

export async function POST(request) {
  try {
    const body = await request.json();
    const {
      tx_ref,
      amount,
      currency = "NGN",
      email,
      phone_number,
      name,
      payment_options = "card,mobilemoney,ussd,banktransfer",
      meta = {},
      customizations = {},
    } = body;

    if (!amount || !email || !name) {
      return NextResponse.json(
        {
          success: false,
          message: "Missing required fields: amount, email, name",
        },
        { status: 400 }
      );
    }

    // Generate unique transaction ref
    // const tx_ref = `TX-${Date.now()}-${Math.random()
    //   .toString(36)
    //   .substr(2, 9)}`;

    // Build payload
    const payload = {
      tx_ref,
      amount: parseFloat(amount),
      currency,
      redirect_url: `${process.env.NEXT_PUBLIC_BASE_URL}/payment/callback`,
      payment_options,
      customer: {
        email,
        phone_number,
        name,
        meta,
        user_id: String(meta.user_id),
        plan: String(meta.plan),
      },
      customizations: {
        title: customizations.title || "Payment",
        description: customizations.description || "Payment for services",
        // logo: customizations.logo || "",
      },
      meta,
    };

    console.log(meta);

    // Call Flutterwave API
    const response = await fetch("https://api.flutterwave.com/v3/payments", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${process.env.FLUTTERWAVE_SECRET_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const result = await response.json();

    if (result.status === "success") {
      return NextResponse.json({
        success: true,
        data: {
          link: result.data.link,
          tx_ref: tx_ref,
          payment_id: result.data.id,
        },
      });
    } else {
      return NextResponse.json(
        {
          success: false,
          message: result.message || "Payment initialization failed",
        },
        { status: 400 }
      );
    }
  } catch (error) {
    console.error("Payment initialization error:", error.message);
    return NextResponse.json(
      {
        success: false,
        message: "Internal server error",
        error:
          process.env.NODE_ENV === "development"
            ? error.message
            : "Payment failed",
      },
      { status: 500 }
    );
  }
}
