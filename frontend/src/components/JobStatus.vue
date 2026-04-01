<template>
  <tr>
    <td class="job-name">{{ job.job_name }}</td>
    <td>{{ job.category }}</td>
    <td>
      <span :class="['badge', `badge--${job.status}`]">{{ statusLabel(job.status) }}</span>
    </td>
    <td class="time">{{ job.last_run ? formatDate(job.last_run) : "—" }}</td>
    <td class="time">{{ job.next_run ? formatDate(job.next_run) : "—" }}</td>
  </tr>
</template>

<script setup>
defineProps({
  job: {
    type: Object,
    required: true,
  },
});

const STATUS_LABELS = {
  success: "成功",
  running: "実行中",
  idle: "待機中",
  failed: "失敗",
};

function statusLabel(status) {
  return STATUS_LABELS[status] ?? status;
}

function formatDate(iso) {
  return new Date(iso).toLocaleString("ja-JP", {
    timeZone: "Asia/Tokyo",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}
</script>

<style scoped>
td {
  padding: 8px 12px;
  border-bottom: 1px solid #e2e8f0;
  font-size: 0.85rem;
  color: #2d3748;
  vertical-align: middle;
}
.job-name {
  font-family: monospace;
  font-size: 0.8rem;
  color: #4a5568;
}
.time {
  font-size: 0.75rem;
  color: #718096;
  white-space: nowrap;
}
.badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
}
.badge--success { background: #c6f6d5; color: #276749; }
.badge--running { background: #bee3f8; color: #2b6cb0; }
.badge--idle    { background: #e2e8f0; color: #4a5568; }
.badge--failed  { background: #fed7d7; color: #9b2c2c; }
</style>
