export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        space: "#070b14",
        panel: "#101827",
        line: "#263244",
        cyan: "#22d3ee",
        amber: "#f59e0b",
        danger: "#ef4444"
      },
      boxShadow: {
        glow: "0 0 28px rgba(34, 211, 238, 0.15)"
      }
    }
  },
  plugins: []
};
