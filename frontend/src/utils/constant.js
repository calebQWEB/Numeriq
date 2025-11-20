export const plans = [
  {
    name: "Free",
    figure: 0,
    price: "$0",
    credits: "Manual Analysis Only",
    features: [
      { text: "Basic spreadsheet analysis", included: true },
      { text: "No credits included", included: true },
      { text: "AI Analysis", included: false },
      { text: "Chat system", included: false },
      { text: "Export insights to PDF", included: false },
    ],
  },
  {
    name: "Plus",
    figure: 25,
    price: "$25/month",
    credits: "50,000 credits",
    features: [
      { text: "Basic spreadsheet analysis", included: true },
      { text: "AI-powered analysis", included: true },
      { text: "Chat system", included: true },
      { text: "Export insights to PDF", included: false },
    ],
    isPopular: true,
  },
  {
    name: "Pro",
    price: "$50/month",
    figure: 50,
    credits: "100,000 credits",
    features: [
      { text: "Basic spreadsheet analysis", included: true },
      { text: "AI-powered analysis", included: true },
      { text: "Chat system", included: true },
      { text: "Export insights to PDF", included: true },
    ],
  },
];
