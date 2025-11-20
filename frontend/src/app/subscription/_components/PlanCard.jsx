"use client";

import React from "react";

const CheckIcon = ({ className = "" }) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    fill="currentColor"
    className={`w-5 h-5 text-emerald-500 ${className}`}
  >
    <path
      fillRule="evenodd"
      d="M19.916 4.626a.75.75 0 01.208 1.04l-9.5 13.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 8.85-12.631a.75.75 0 011.04-.208z"
      clipRule="evenodd"
    />
  </svg>
);

const XMarkIcon = ({ className = "" }) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    fill="none"
    viewBox="0 0 24 24"
    strokeWidth={1.5}
    stroke="currentColor"
    className={`w-5 h-5 text-red-500 ${className}`}
  >
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      d="M6 18L18 6M6 6l12 12"
    />
  </svg>
);

export default function PlanCard({ plan, setChosenPlan, initializePayment }) {
  const isPopular = plan.isPopular;
  const cardClasses = `
    flex flex-col p-8 rounded-3xl shadow-2xl transition-all duration-300
    hover:scale-105 hover:shadow-2xl
    ${
      isPopular
        ? "bg-gradient-to-br from-blue-600 to-indigo-700 text-white transform scale-105 border-4 border-yellow-300"
        : "bg-gray-800 text-gray-200"
    }
  `;

  const priceClasses = isPopular
    ? "text-4xl sm:text-5xl font-extrabold text-white"
    : "text-4xl sm:text-5xl font-extrabold text-white";

  const featureTextClasses = isPopular ? "text-gray-200" : "text-gray-300";

  return (
    <div className={cardClasses}>
      {isPopular && (
        <span className="absolute -top-3 -right-3 rounded-full bg-yellow-400 text-gray-900 px-4 py-1 text-sm font-bold shadow-lg">
          Most Popular
        </span>
      )}
      <div className="flex-grow">
        <h3 className="text-3xl font-bold tracking-tight mb-2">{plan.name}</h3>
        <p className="mb-6 font-semibold opacity-75">{plan.credits}</p>
        <p className={priceClasses}>{plan.price}</p>
        <ul className="space-y-4 mt-8 text-lg font-medium">
          {plan.features.map((feature, index) => (
            <li key={index} className="flex items-center space-x-3">
              {feature.included ? <CheckIcon /> : <XMarkIcon />}
              <span className={featureTextClasses}>{feature.text}</span>
            </li>
          ))}
        </ul>
      </div>
      <button
        onClick={() => {
          initializePayment(plan.name, plan.figure);
        }}
        className={`mt-10 w-full rounded-full py-4 px-6 text-lg font-bold transition duration-300 transform hover:scale-105
          ${
            isPopular
              ? "bg-yellow-400 text-gray-900 shadow-md hover:bg-yellow-300"
              : "bg-indigo-600 text-white shadow-md hover:bg-indigo-500"
          }
        `}
      >
        Choose Plan
      </button>
    </div>
  );
}
