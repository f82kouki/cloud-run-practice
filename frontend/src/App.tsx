import { useEffect, useState } from "react";
import DashboardStats from "./components/DashboardStats";
import StudentCard from "./components/StudentCard";
import ScoutList from "./components/ScoutList";
import type { DashboardStats as Stats, Student, ScoutMessage } from "./types";

type Tab = "dashboard" | "students" | "scouts";

const TABS: { key: Tab; label: string }[] = [
  { key: "dashboard", label: "ダッシュボード" },
  { key: "students", label: "学生検索" },
  { key: "scouts", label: "スカウト管理" },
];

export default function App() {
  const [tab, setTab] = useState<Tab>("dashboard");
  const [stats, setStats] = useState<Stats | null>(null);
  const [students, setStudents] = useState<Student[]>([]);
  const [scouts, setScouts] = useState<ScoutMessage[]>([]);
  const [scoutFilter, setScoutFilter] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([
      fetch("/api/dashboard").then((r) => r.json()),
      fetch("/api/students").then((r) => r.json()),
      fetch("/api/scouts").then((r) => r.json()),
    ])
      .then(([d, s, sc]) => {
        setStats(d);
        setStudents(s);
        setScouts(sc);
      })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  const filteredScouts = scoutFilter
    ? scouts.filter((s) => s.status === scoutFilter)
    : scouts;

  const scoutCounts: Record<string, number> = {
    "": scouts.length,
    pending: scouts.filter((s) => s.status === "pending").length,
    opened: scouts.filter((s) => s.status === "opened").length,
    accepted: scouts.filter((s) => s.status === "accepted").length,
    declined: scouts.filter((s) => s.status === "declined").length,
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center text-gray-400">
        読み込み中...
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center text-red-500">
        エラー: {error}
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="bg-gray-900 text-white">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <h1 className="text-lg font-bold tracking-tight">ScoutConnect</h1>
            <span className="text-xs bg-gray-700 px-2.5 py-0.5 rounded-full">企業管理画面</span>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-sm text-gray-400">株式会社サンプル</span>
            <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-sm font-bold">
              S
            </div>
          </div>
        </div>
      </header>

      {/* Tabs */}
      <nav className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6 flex gap-1">
          {TABS.map((t) => (
            <button
              key={t.key}
              onClick={() => setTab(t.key)}
              className={`px-4 py-3 text-sm font-medium border-b-2 transition-colors ${
                tab === t.key
                  ? "border-blue-600 text-blue-600"
                  : "border-transparent text-gray-500 hover:text-gray-700"
              }`}
            >
              {t.label}
            </button>
          ))}
        </div>
      </nav>

      {/* Content */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        {tab === "dashboard" && stats && (
          <div className="space-y-8">
            <div>
              <h2 className="text-lg font-bold text-gray-800 mb-4">概要</h2>
              <DashboardStats stats={stats} />
            </div>
            <div>
              <h2 className="text-lg font-bold text-gray-800 mb-4">最近のスカウト</h2>
              <ScoutList
                scouts={scouts.slice(0, 5)}
                currentFilter=""
                onFilter={() => {
                  setTab("scouts");
                }}
                counts={scoutCounts}
              />
            </div>
          </div>
        )}

        {tab === "students" && (
          <div>
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-lg font-bold text-gray-800">
                学生一覧
                <span className="ml-2 text-sm font-normal text-gray-400">{students.length}名</span>
              </h2>
            </div>
            <div className="space-y-4">
              {students.map((s) => (
                <StudentCard key={s.id} student={s} />
              ))}
            </div>
          </div>
        )}

        {tab === "scouts" && (
          <div>
            <h2 className="text-lg font-bold text-gray-800 mb-4">スカウト管理</h2>
            <ScoutList
              scouts={filteredScouts}
              currentFilter={scoutFilter}
              onFilter={setScoutFilter}
              counts={scoutCounts}
            />
          </div>
        )}
      </main>
    </div>
  );
}
