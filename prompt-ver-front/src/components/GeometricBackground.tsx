export function GeometricBackground() {
  return (
    <div className="fixed inset-0 -z-10 overflow-hidden pointer-events-none">
      <svg
        className="absolute inset-0 w-full h-full"
        xmlns="http://www.w3.org/2000/svg"
        preserveAspectRatio="xMidYMid slice"
      >
        <defs>
          <pattern id="grid" width="60" height="60" patternUnits="userSpaceOnUse">
            <path
              d="M 60 0 L 0 0 0 60"
              fill="none"
              className="stroke-gray-200 dark:stroke-gray-800"
              strokeWidth="0.5"
            />
          </pattern>
          <radialGradient id="fade" cx="50%" cy="50%" r="60%">
            <stop offset="0%" stopColor="transparent" />
            <stop offset="100%" stopColor="white" className="dark:stop-color-gray-950" />
          </radialGradient>
        </defs>
        <rect width="100%" height="100%" fill="url(#grid)" />
        <circle cx="10%" cy="20%" r="300" className="fill-blue-500/5 dark:fill-blue-400/5" />
        <circle cx="90%" cy="80%" r="400" className="fill-cyan-500/5 dark:fill-cyan-400/5" />
        <circle cx="80%" cy="10%" r="200" className="fill-teal-500/5 dark:fill-teal-400/5" />
        <polygon
          points="200,100 350,300 50,300"
          className="fill-blue-400/5 dark:fill-blue-300/5"
        />
        <polygon
          points="1200,500 1400,800 1000,800"
          className="fill-cyan-400/5 dark:fill-cyan-300/5"
        />
      </svg>
    </div>
  );
}
