import type { ScoutMessage } from "../types";

const STATUS_MAP: Record<ScoutMessage["status"], { label: string; cls: string }> = {
  pending:  { label: "未開封", cls: "bg-gray-100 text-gray-600" },
  opened:   { label: "開封済", cls: "bg-blue-100 text-blue-700" },
  accepted: { label: "承認",   cls: "bg-green-100 text-green-700" },
  declined: { label: "辞退",   cls: "bg-red-100 text-red-700" },
};

const FILTERS: { value: string; label: string }[] = [
  { value: "",         label: "すべて" },
  { value: "pending",  label: "未開封" },
  { value: "opened",   label: "開封済" },
  { value: "accepted", label: "承認" },
  { value: "declined", label: "辞退" },
];

function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString("ja-JP", {
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}

type Props = {
  scouts: ScoutMessage[];
  currentFilter: string;
  onFilter: (v: string) => void;
  counts: Record<string, number>;
};

export default function ScoutList({ scouts, currentFilter, onFilter, counts }: Props) {
  return (
    <div>
      {/* Filters */}
      <div className="flex flex-wrap gap-2 mb-4">
        {FILTERS.map((f) => (
          <button
            key={f.value}
            onClick={() => onFilter(f.value)}
            className={`px-4 py-1.5 rounded-full text-sm font-medium border transition-colors flex items-center gap-1.5 ${
              currentFilter === f.value
                ? "bg-blue-600 text-white border-blue-600"
                : "bg-gray-50 text-gray-600 border-gray-200 hover:bg-gray-100"
            }`}
          >
            {f.label}
            <span
              className={`text-xs px-1.5 py-0.5 rounded-full ${
                currentFilter === f.value ? "bg-white/25" : "bg-black/5"
              }`}
            >
              {counts[f.value] ?? 0}
            </span>
          </button>
        ))}
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full bg-white rounded-xl border border-gray-200 overflow-hidden">
          <thead className="bg-gray-50">
            <tr>
              {["学生名", "大学", "件名", "ステータス", "送信日", "返信日"].map((h) => (
                <th key={h} className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wide">
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {scouts.map((s) => {
              const st = STATUS_MAP[s.status];
              return (
                <tr key={s.id} className="border-t border-gray-100 hover:bg-gray-50 transition-colors">
                  <td className="px-4 py-3 font-semibold text-sm whitespace-nowrap">{s.student_name}</td>
                  <td className="px-4 py-3 text-sm text-gray-500 whitespace-nowrap">{s.student_university}</td>
                  <td className="px-4 py-3 text-sm max-w-[300px] truncate">{s.subject}</td>
                  <td className="px-4 py-3">
                    <span className={`text-xs font-bold px-2.5 py-1 rounded-full ${st.cls}`}>{st.label}</span>
                  </td>
                  <td className="px-4 py-3 text-xs text-gray-400 whitespace-nowrap">{formatDate(s.sent_at)}</td>
                  <td className="px-4 py-3 text-xs text-gray-400 whitespace-nowrap">
                    {s.responded_at ? formatDate(s.responded_at) : "—"}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
