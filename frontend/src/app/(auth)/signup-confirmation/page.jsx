import Link from "next/link";

export default function SignupConfirmation() {
  return (
    <section className="min-h-screen flex items-center justify-center bg-gray-900 font-inter">
      <div className="flex items-center justify-center flex-col gap-5 relative w-full max-w-xl mx-auto p-8 shadow-lg bg-white/10 backdrop-blur-md border rounded-3xl border-white/20 text-center">
        <h2 className="text-4xl font-extrabold text-green-600 mb-4 tracking-tight">
          Signup Successful!
        </h2>
        <p className="text-lg">
          Thank you for signing up! A confirmation email has been sent to your
          email address. Please check your inbox and click the confirmation link
          to verify your account.
        </p>

        <Link
          href="/login"
          className="cursor-pointer w-full px-6 py-3 mt-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-bold text-lg rounded-lg shadow-lg hover:from-blue-700 hover:to-purple-700 transition-all duration-300 ease-in-out transform hover:scale-105 focus:outline-none focus:ring-4 focus:ring-blue-300 focus:ring-opacity-75"
        >
          Proceed to Login
        </Link>
      </div>
    </section>
  );
}
