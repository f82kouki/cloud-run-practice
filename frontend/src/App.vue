<template>
  <div class="app">
    <header class="header">
      <h1>Cloud Run Practice Dashboard</h1>
      <span class="env-badge">{{ env }}</span>
    </header>

    <main class="main">
      <!-- Metrics -->
      <section class="section">
        <h2>プラットフォームメトリクス</h2>
        <div v-if="metricsLoading" class="loading">読み込み中...</div>
        <div v-else-if="metricsError" class="error">{{ metricsError }}</div>
        <div v-else class="metrics-grid">
          <MetricsCard v-for="m in metrics" :key="m.platform" :metrics="m" />
        </div>
      </section>

      <!-- Jobs -->
      <section class="section">
        <h2>ジョブ一覧</h2>
        <div v-if="jobsLoading" class="loading">読み込み中...</div>
        <div v-else-if="jobsError" class="error">{{ jobsError }}</div>
        <div v-else class="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>ジョブ名</th>
                <th>カテゴリ</th>
                <th>ステータス</th>
                <th>最終実行</th>
                <th>次回実行</th>
              </tr>
            </thead>
            <tbody>
              <JobStatus v-for="job in jobs" :key="job.job_name" :job="job" />
            </tbody>
          </table>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import MetricsCard from "./components/MetricsCard.vue";
import JobStatus from "./components/JobStatus.vue";

const env = import.meta.env.VITE_ENV ?? "local";

const metrics = ref([]);
const metricsLoading = ref(true);
const metricsError = ref(null);

const jobs = ref([]);
const jobsLoading = ref(true);
const jobsError = ref(null);

async function fetchMetrics() {
  try {
    const res = await fetch("/api/metrics");
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    metrics.value = await res.json();
  } catch (e) {
    metricsError.value = `メトリクスの取得に失敗しました: ${e.message}`;
  } finally {
    metricsLoading.value = false;
  }
}

async function fetchJobs() {
  try {
    const res = await fetch("/api/jobs");
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    jobs.value = await res.json();
  } catch (e) {
    jobsError.value = `ジョブ一覧の取得に失敗しました: ${e.message}`;
  } finally {
    jobsLoading.value = false;
  }
}

onMounted(() => {
  fetchMetrics();
  fetchJobs();
});
</script>

<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #f7fafc; color: #1a202c; }
</style>

<style scoped>
.app { min-height: 100vh; }

.header {
  background: #2d3748;
  color: #fff;
  padding: 16px 32px;
  display: flex;
  align-items: center;
  gap: 12px;
}
.header h1 { font-size: 1.25rem; }
.env-badge {
  background: #4a5568;
  padding: 2px 10px;
  border-radius: 12px;
  font-size: 0.75rem;
  text-transform: uppercase;
}

.main { padding: 32px; max-width: 1200px; margin: 0 auto; }

.section { margin-bottom: 40px; }
.section h2 { font-size: 1.1rem; font-weight: 700; margin-bottom: 16px; color: #2d3748; }

.metrics-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.table-wrapper { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; background: #fff; border-radius: 8px; overflow: hidden; border: 1px solid #e2e8f0; }
thead { background: #edf2f7; }
th { padding: 10px 12px; text-align: left; font-size: 0.8rem; font-weight: 600; color: #4a5568; }

.loading { color: #718096; }
.error { color: #e53e3e; }
</style>
