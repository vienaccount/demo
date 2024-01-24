export default function StatRadial({
  size = 60,
  value = 50,
}: {
  size?: number;
  value?: number;
}) {
  const angle = 360;
  const fractionText = `${value}`;

  const backgroundColor = "hsl(var(--accent))";
  const progressColor = "hsl(var(--warning-dark))";
  const progressColorUnfilled = "hsl(var(--warning-light))";

  return (
    <div
      style={{
        background: `
                radial-gradient(${backgroundColor} 55%, transparent 56%),
                conic-gradient(${progressColor} 0deg ${angle}deg, ${progressColorUnfilled} ${angle}deg 360deg),
                ${backgroundColor}`,
        borderRadius: "50%",
        width: `${size}px`,
        height: `${size}px`,
      }}
    >
      <div className="flex w-full h-full text-sm justify-center items-center text-center p-0">
        {fractionText}
      </div>
    </div>
  );
}
