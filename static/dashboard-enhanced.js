// Enhanced Persona Manager Dashboard with improved UI/UX
// Safe enhancement - no MCP protocol impact

// Enhanced utility functions
const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
};

const formatNumber = (num) => {
  if (num >= 1000000) return (num / 1000000).toFixed(1) + "M";
  if (num >= 1000) return (num / 1000).toFixed(1) + "K";
  return num.toString();
};

const getConfidenceColor = (confidence) => {
  if (confidence >= 0.8) return "#10b981";
  if (confidence >= 0.6) return "#f59e0b";
  return "#ef4444";
};

// Enhanced loading component
const LoadingSpinner = ({ size = "medium", text = "Loading..." }) => {
  const sizeClasses = {
    small: "w-4 h-4",
    medium: "w-8 h-8",
    large: "w-12 h-12",
  };

  return `<div class="flex flex-col items-center justify-center p-4">
      <div class="${sizeClasses[size]} animate-spin rounded-full border-4 border-gray-200 border-t-purple-600"></div>
      <p class="mt-2 text-sm text-gray-600">${text}</p>
    </div>`;
};

// Enhanced error component
const ErrorDisplay = (error, onRetry) => {
  return `
    <div class="bg-red-50 border border-red-200 rounded-lg p-4">
      <div class="flex items-center">
        <i class="fas fa-exclamation-triangle text-red-400 mr-2"></i>
        <h3 class="text-sm font-medium text-red-800">Error</h3>
      </div>
      <p class="mt-1 text-sm text-red-700">${error}</p>
      ${
        onRetry
          ? `
        <button onclick="${onRetry}" class="mt-2 bg-red-600 text-white px-3 py-1 rounded text-sm hover:bg-red-700">
          Retry
        </button>
      `
          : ""
      }
    </div>
  `;
};

// Enhanced status indicator
const StatusIndicator = (status) => {
  const getStatusColor = (status) => {
    switch (status) {
      case "connected":
        return "bg-green-500";
      case "connecting":
        return "bg-yellow-500";
      case "disconnected":
        return "bg-red-500";
      default:
        return "bg-gray-500";
    }
  };

  return `
    <div class="flex items-center space-x-2">
      <div class="w-2 h-2 rounded-full ${getStatusColor(status)} animate-pulse"></div>
      <span class="text-sm text-gray-600 capitalize">${status}</span>
    </div>
  `;
};

// Enhanced persona card component
const PersonaCard = (persona) => {
  const confidence = persona.confidence || 0;
  const confidenceColor = getConfidenceColor(confidence);

  return `
    <div class="bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow duration-200">
      <div class="p-6">
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center">
            <div class="w-10 h-10 bg-purple-100 rounded-full flex items-center justify-center">
              <i class="fas fa-user-tie text-purple-600"></i>
            </div>
            <div class="ml-3">
              <h3 class="text-lg font-semibold text-gray-900">${persona.name}</h3>
              <p class="text-sm text-gray-500">${persona.description || "No description"}</p>
            </div>
          </div>
          <div class="text-right">
            <div class="text-sm font-medium text-gray-600">Confidence</div>
            <div class="text-lg font-bold" style="color: ${confidenceColor}">${(confidence * 100).toFixed(0)}%</div>
          </div>
        </div>
        
        <div class="space-y-2">
          <div class="flex items-center text-sm text-gray-600">
            <i class="fas fa-tag text-purple-400 mr-2"></i>
            <span class="font-medium">Expertise:</span>
            <span class="ml-1">${persona.expertise?.join(", ") || "General"}</span>
          </div>
          
          <div class="flex items-center text-sm text-gray-600">
            <i class="fas fa-clock text-purple-400 mr-2"></i>
            <span class="font-medium">Last Used:</span>
            <span class="ml-1">${persona.last_used ? formatDate(persona.last_used) : "Never"}</span>
          </div>
          
          <div class="flex items-center text-sm text-gray-600">
            <i class="fas fa-chart-line text-purple-400 mr-2"></i>
            <span class="font-medium">Usage Count:</span>
            <span class="ml-1">${formatNumber(persona.usage_count || 0)}</span>
          </div>
        </div>
        
        <div class="mt-4 pt-4 border-t border-gray-200">
          <div class="flex justify-between items-center">
            <button class="bg-purple-600 text-white px-3 py-1 rounded text-sm hover:bg-purple-700 transition-colors">
              Select
            </button>
            <button class="text-purple-600 hover:text-purple-700 text-sm font-medium">
              View Details
            </button>
          </div>
        </div>
      </div>
    </div>
  `;
};

// Enhanced analytics chart component
const AnalyticsChart = (data, type = "bar") => {
  const canvasId = `chart-${Date.now()}`;

  return `
    <div class="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
      <h3 class="text-lg font-semibold text-gray-900 mb-4">Persona Analytics</h3>
      <canvas id="${canvasId}" height="300"></canvas>
    </div>
    <script>
      const ctx = document.getElementById('${canvasId}').getContext('2d');
      new Chart(ctx, {
        type: '${type}',
        data: {
          labels: ${JSON.stringify(data.labels || [])},
          datasets: [{
            label: 'Usage Count',
            data: ${JSON.stringify(data.values || [])},
            backgroundColor: 'rgba(147, 51, 234, 0.2)',
            borderColor: 'rgba(147, 51, 234, 1)',
            borderWidth: 2
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: true,
              position: 'top'
            }
          },
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      });
    </script>
  `;
};

// Main enhanced dashboard functionality
class EnhancedPersonaDashboard {
  constructor() {
    this.data = {
      personas: [],
      analytics: {},
      recentActivity: [],
      systemHealth: {},
    };
    this.loading = true;
    this.error = null;
    this.activeTab = "overview";
    this.refreshInterval = 30000; // 30 seconds
    this.refreshTimer = null;

    this.init();
  }

  async init() {
    await this.fetchData();
    this.setupEventListeners();
    this.startAutoRefresh();
    this.render();
  }

  async fetchData() {
    try {
      this.loading = true;
      this.error = null;

      const [personasRes, analyticsRes, activityRes, healthRes] = await Promise.all([
        fetch("/personas"),
        fetch("/analytics/overview"),
        fetch("/activity/recent"),
        fetch("/health"),
      ]);

      if (!personasRes.ok || !analyticsRes.ok || !activityRes.ok || !healthRes.ok) {
        throw new Error("Failed to fetch dashboard data");
      }

      const [personas, analytics, activity, health] = await Promise.all([
        personasRes.json(),
        analyticsRes.json(),
        activityRes.json(),
        healthRes.json(),
      ]);

      this.data = {
        personas: personas.data?.personas || [],
        analytics: analytics.data || {},
        recentActivity: activity.data?.activities || [],
        systemHealth: health.data || {},
      };
    } catch (err) {
      this.error = err.message;
      console.error("Dashboard data fetch error:", err);
    } finally {
      this.loading = false;
    }
  }

  setupEventListeners() {
    // Tab switching
    document.querySelectorAll("[data-tab]").forEach((button) => {
      button.addEventListener("click", (e) => {
        this.activeTab = e.target.dataset.tab;
        this.render();
      });
    });

    // Refresh button
    const refreshBtn = document.getElementById("refresh-btn");
    if (refreshBtn) {
      refreshBtn.addEventListener("click", () => this.fetchData());
    }

    // Auto-refresh interval selector
    const intervalSelect = document.getElementById("refresh-interval");
    if (intervalSelect) {
      intervalSelect.addEventListener("change", (e) => {
        this.refreshInterval = Number(e.target.value);
        this.startAutoRefresh();
      });
    }
  }

  startAutoRefresh() {
    if (this.refreshTimer) {
      clearInterval(this.refreshTimer);
    }
    this.refreshTimer = setInterval(() => this.fetchData(), this.refreshInterval);
  }

  render() {
    const mainContent = document.getElementById("main-content");
    if (!mainContent) return;

    if (this.loading && !this.data.personas.length) {
      mainContent.innerHTML = LoadingSpinner("large", "Loading dashboard...");
      return;
    }

    if (this.error) {
      mainContent.innerHTML = ErrorDisplay(this.error, () => this.fetchData());
      return;
    }

    switch (this.activeTab) {
      case "overview":
        mainContent.innerHTML = this.renderOverview();
        break;
      case "personas":
        mainContent.innerHTML = this.renderPersonas();
        break;
      case "analytics":
        mainContent.innerHTML = this.renderAnalytics();
        break;
      case "activity":
        mainContent.innerHTML = this.renderActivity();
        break;
    }

    this.updateLastUpdated();
  }

  renderOverview() {
    const stats = this.data.analytics;

    return `
      <div class="space-y-6">
        <!-- Enhanced Stats Cards -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div class="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <i class="fas fa-users text-purple-600 text-2xl"></i>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">Total Personas</p>
                <p class="text-2xl font-bold text-gray-900">${formatNumber(this.data.personas.length)}</p>
              </div>
            </div>
          </div>
          
          <div class="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <i class="fas fa-mouse-pointer text-purple-600 text-2xl"></i>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">Total Selections</p>
                <p class="text-2xl font-bold text-gray-900">${formatNumber(stats.total_selections || 0)}</p>
              </div>
            </div>
          </div>
          
          <div class="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <i class="fas fa-bullseye text-purple-600 text-2xl"></i>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">Avg Confidence</p>
                <p class="text-2xl font-bold text-gray-900">${((stats.avg_confidence || 0) * 100).toFixed(0)}%</p>
              </div>
            </div>
          </div>
          
          <div class="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <i class="fas fa-robot text-purple-600 text-2xl"></i>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">Active Personas</p>
                <p class="text-2xl font-bold text-gray-900">${formatNumber(stats.active_personas || 0)}</p>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Enhanced Charts -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          ${AnalyticsChart(
            {
              labels: this.data.personas.slice(0, 10).map((p) => p.name),
              values: this.data.personas.slice(0, 10).map((p) => p.usage_count || 0),
            },
            "bar",
          )}
          
          ${AnalyticsChart(
            {
              labels: this.data.recentActivity.map((a) => formatDate(a.timestamp)),
              values: this.data.recentActivity.map((a) => a.count || 0),
            },
            "line",
          )}
        </div>
      </div>
    `;
  }

  renderPersonas() {
    return `
      <div class="bg-white rounded-lg shadow-sm border border-gray-200">
        <div class="px-6 py-4 border-b border-gray-200">
          <h2 class="text-lg font-semibold text-gray-900">All Personas</h2>
          <p class="text-sm text-gray-600 mt-1">${this.data.personas.length} personas available</p>
        </div>
        <div class="p-6">
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            ${this.data.personas.map((persona) => PersonaCard(persona)).join("")}
          </div>
        </div>
      </div>
    `;
  }

  renderAnalytics() {
    return `
      <div class="space-y-6">
        <div class="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
          <h2 class="text-lg font-semibold text-gray-900 mb-4">Detailed Analytics</h2>
          <pre class="bg-gray-50 p-4 rounded-lg overflow-auto text-sm">${JSON.stringify(
            this.data.analytics,
            null,
            2,
          )}</pre>
        </div>
      </div>
    `;
  }

  renderActivity() {
    return `
      <div class="bg-white rounded-lg shadow-sm border border-gray-200">
        <div class="px-6 py-4 border-b border-gray-200">
          <h2 class="text-lg font-semibold text-gray-900">Recent Activity</h2>
        </div>
        <div class="divide-y divide-gray-200">
          ${this.data.recentActivity
            .map(
              (activity, index) => `
            <div class="px-6 py-4">
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-sm font-medium text-gray-900">${activity.action}</p>
                  <p class="text-sm text-gray-500">${activity.description}</p>
                </div>
                <span class="text-sm text-gray-500">${formatDate(activity.timestamp)}</span>
              </div>
            </div>
          `,
            )
            .join("")}
        </div>
      </div>
    `;
  }

  updateLastUpdated() {
    const lastUpdated = document.getElementById("last-updated");
    if (lastUpdated) {
      lastUpdated.textContent = `Last updated: ${formatDate(new Date())}`;
    }
  }
}

// Initialize enhanced dashboard when DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  new EnhancedPersonaDashboard();
});
