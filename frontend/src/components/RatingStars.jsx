import React, { useState } from 'react';
import { Star } from 'lucide-react';

/**
 * Reusable Star Rating component with interactive review input support
 * and high-fidelity dark glassmorphic styling.
 *
 * @param {number} rating - Current numeric rating (0 to 5).
 * @param {number} maxRating - Total number of stars (default: 5).
 * @param {boolean} interactive - Whether users can hover & click to set rating.
 * @param {Function} onChange - Callback when rating changes in interactive mode.
 * @param {string} size - Size class for stars (e.g. 'w-4 h-4', 'w-5 h-5').
 * @param {boolean} showValue - Whether to display numeric rating text next to stars.
 */
export function RatingStars({
  rating = 0,
  maxRating = 5,
  interactive = false,
  onChange = () => {},
  size = 'w-4 h-4',
  showValue = false,
  className = '',
}) {
  const [hoverRating, setHoverRating] = useState(0);

  const displayRating = interactive && hoverRating > 0 ? hoverRating : rating;

  return (
    <div className={`inline-flex items-center gap-1.5 ${className}`}>
      <div className="flex items-center gap-0.5">
        {Array.from({ length: maxRating }, (_, index) => {
          const starValue = index + 1;
          const isFilled = displayRating >= starValue;
          const isHalf = !isFilled && displayRating >= starValue - 0.5;

          return (
            <button
              key={index}
              type="button"
              disabled={!interactive}
              onClick={() => interactive && onChange(starValue)}
              onMouseEnter={() => interactive && setHoverRating(starValue)}
              onMouseLeave={() => interactive && setHoverRating(0)}
              className={`transition-transform ${
                interactive
                  ? 'cursor-pointer hover:scale-115 focus:outline-none focus-visible:ring-1 focus-visible:ring-cyan-400 rounded-sm'
                  : 'cursor-default'
              }`}
              aria-label={`${starValue} out of ${maxRating} stars`}
            >
              <Star
                className={`${size} transition-colors duration-150 ${
                  isFilled
                    ? 'fill-amber-400 text-amber-400 drop-shadow-[0_0_8px_rgba(251,191,36,0.5)]'
                    : isHalf
                    ? 'fill-amber-400/50 text-amber-400'
                    : 'fill-transparent text-gray-600 dark:text-gray-500'
                }`}
              />
            </button>
          );
        })}
      </div>

      {showValue && (
        <span className="text-xs font-semibold text-gray-300 ml-1">
          {Number(rating).toFixed(1)}
        </span>
      )}
    </div>
  );
}

export default RatingStars;
