<template>
  <div class="card">
    <div class="card-header">
      <span class="platform-name">{{ metrics.platform }}</span>
    </div>
    <div class="card-body">
      <div class="stat">
        <span class="label">フォロワー</span>
        <span class="value">{{ formatNumber(metrics.followers) }}</span>
      </div>
      <div class="stat">
        <span class="label">投稿数</span>
        <span class="value">{{ formatNumber(metrics.posts) }}</span>
      </div>
      <div class="stat">
        <span class="label">エンゲージメント率</span>
        <span class="value">{{ metrics.engagement_rate }}%</span>
      </div>
    </div>
    <div class="card-footer">
      収集日時: {{ formatDate(metrics.collected_at) }}
    </div>
  </div>
</template>

<script setup>
defineProps({
  metrics: {
    type: Object,
    required: true,
  },
});

function formatNumber(n) {
  return n.toLocaleString("ja-JP");
}

function formatDate(iso) {
  return new Date(iso).toLocaleString("ja-JP", { timeZone: "Asia/Tokyo" });
}
</script>

<style scoped>
.card {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 16px;
  min-width: 200px;
}
.card-header {
  margin-bottom: 12px;
}
.platform-name {
  font-size: 1.1rem;
  font-weight: 700;
  color: #1a202c;
}
.card-body {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.stat {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.label {
  font-size: 0.8rem;
  color: #718096;
}
.value {
  font-size: 1rem;
  font-weight: 600;
  color: #2d3748;
}
.card-footer {
  margin-top: 12px;
  font-size: 0.75rem;
  color: #a0aec0;
}
</style>
