import type { DashboardStats as Stats } from "../types";

const cards = [
  { key: "total_scouts_sent", label: "スカウト送信数", unit: "通", color: "text-gray-900" },
  { key: "open_rate", label: "開封率", unit: null, color: "text-blue-600", suffix: "%" },
  { key: "accept_rate", label: "承認率", unit: null, color: "text-green-600", suffix: "%" },
  { key: "scouts_declined", label: "辞退数", unit: "件", color: "text-red-500" },
  { key: "active_students", label: "アクティブ学生数", unit: "名", color: "text-gray-900" },
  { key: "new_students_this_week", label: "今週の新規登録", unit: "名", color: "text-purple-600", prefix: "+" },
] as const;

export default function DashboardStats({ stats }: { stats: Stats }) {
  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
      {cards.map((c) => {
        const val = stats[c.key as keyof Stats];
        return (
          <div key={c.key} className="bg-white rounded-xl border border-gray-200 p-5 text-center">
            <p className="text-xs text-gray-500 mb-2">{c.label}</p>
            <p className={`text-2xl font-extrabold ${c.color}`}>
              {"prefix" in c ? c.prefix : ""}
              {val.toLocaleString("ja-JP")}
              {"suffix" in c ? c.suffix : ""}
            </p>
            {c.unit && <p className="text-xs text-gray-400 mt-1">{c.unit}</p>}
          </div>
        );
      })}
    </div>
  );
}
