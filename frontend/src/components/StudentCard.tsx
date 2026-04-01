import type { Student } from "../types";

function timeAgo(iso: string): string {
  const diff = Math.floor((Date.now() - new Date(iso).getTime()) / (1000 * 60 * 60));
  if (diff < 1) return "1時間以内";
  if (diff < 24) return `${diff}時間前`;
  const days = Math.floor(diff / 24);
  if (days < 7) return `${days}日前`;
  return new Date(iso).toLocaleDateString("ja-JP");
}

export default function StudentCard({ student }: { student: Student }) {
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5 flex gap-4 items-start hover:shadow-md transition-shadow">
      {/* Avatar */}
      <div className="w-12 h-12 rounded-full bg-blue-50 text-blue-600 flex items-center justify-center font-bold text-lg shrink-0">
        {student.name.charAt(0)}
      </div>

      {/* Info */}
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 mb-1">
          <span className="font-bold text-gray-900">{student.name}</span>
          <span className="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full font-semibold">
            {student.graduation_year}卒
          </span>
        </div>
        <p className="text-sm text-gray-500 mb-2">
          {student.university} {student.faculty}
        </p>
        <p className="text-sm text-gray-700 mb-3 leading-relaxed">{student.self_pr}</p>

        {/* Skills */}
        <div className="flex flex-wrap gap-1.5 mb-1.5">
          {student.skills.map((s) => (
            <span key={s} className="text-xs bg-teal-50 text-teal-700 px-2.5 py-0.5 rounded-full font-semibold">
              {s}
            </span>
          ))}
        </div>

        {/* Industries */}
        <div className="flex flex-wrap gap-1.5 mb-2">
          {student.desired_industries.map((ind) => (
            <span key={ind} className="text-xs bg-yellow-50 text-yellow-700 px-2.5 py-0.5 rounded-full font-semibold">
              {ind}
            </span>
          ))}
        </div>

        <p className="text-xs text-gray-400">最終ログイン: {timeAgo(student.last_login)}</p>
      </div>

      {/* Action */}
      <button className="shrink-0 bg-blue-600 hover:bg-blue-700 text-white text-sm font-semibold px-5 py-2 rounded-lg transition-colors">
        スカウトする
      </button>
    </div>
  );
}
