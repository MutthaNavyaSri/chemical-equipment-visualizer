import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar, Line, Pie } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

const DatasetDetail = ({ dataset }) => {
  // Equipment Type Distribution Chart
  const typeLabels = Object.keys(dataset.equipment_types);
  const typeValues = Object.values(dataset.equipment_types);
  
  const pieChartData = {
    labels: typeLabels,
    datasets: [
      {
        label: 'Equipment Count',
        data: typeValues,
        backgroundColor: [
          'rgba(102, 126, 234, 0.8)',
          'rgba(118, 75, 162, 0.8)',
          'rgba(16, 185, 129, 0.8)',
          'rgba(245, 158, 11, 0.8)',
          'rgba(239, 68, 68, 0.8)',
          'rgba(59, 130, 246, 0.8)',
        ],
        borderColor: [
          'rgba(102, 126, 234, 1)',
          'rgba(118, 75, 162, 1)',
          'rgba(16, 185, 129, 1)',
          'rgba(245, 158, 11, 1)',
          'rgba(239, 68, 68, 1)',
          'rgba(59, 130, 246, 1)',
        ],
        borderWidth: 2,
      },
    ],
  };

  // Parameter Comparison Chart
  const equipmentNames = dataset.records.map((r) => r.equipment_name);
  const flowrates = dataset.records.map((r) => r.flowrate);
  const pressures = dataset.records.map((r) => r.pressure);
  const temperatures = dataset.records.map((r) => r.temperature);

  const barChartData = {
    labels: equipmentNames,
    datasets: [
      {
        label: 'Flowrate',
        data: flowrates,
        backgroundColor: 'rgba(102, 126, 234, 0.6)',
        borderColor: 'rgba(102, 126, 234, 1)',
        borderWidth: 2,
      },
      {
        label: 'Pressure',
        data: pressures,
        backgroundColor: 'rgba(118, 75, 162, 0.6)',
        borderColor: 'rgba(118, 75, 162, 1)',
        borderWidth: 2,
      },
      {
        label: 'Temperature',
        data: temperatures,
        backgroundColor: 'rgba(16, 185, 129, 0.6)',
        borderColor: 'rgba(16, 185, 129, 1)',
        borderWidth: 2,
      },
    ],
  };

  const lineChartData = {
    labels: equipmentNames,
    datasets: [
      {
        label: 'Flowrate Trend',
        data: flowrates,
        borderColor: 'rgba(102, 126, 234, 1)',
        backgroundColor: 'rgba(102, 126, 234, 0.1)',
        tension: 0.4,
        fill: true,
      },
      {
        label: 'Pressure Trend',
        data: pressures,
        borderColor: 'rgba(118, 75, 162, 1)',
        backgroundColor: 'rgba(118, 75, 162, 0.1)',
        tension: 0.4,
        fill: true,
      },
      {
        label: 'Temperature Trend',
        data: temperatures,
        borderColor: 'rgba(16, 185, 129, 1)',
        backgroundColor: 'rgba(16, 185, 129, 0.1)',
        tension: 0.4,
        fill: true,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          font: {
            size: 12,
            weight: '600',
          },
          padding: 15,
        },
      },
      title: {
        display: false,
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        grid: {
          color: 'rgba(0, 0, 0, 0.05)',
        },
      },
      x: {
        grid: {
          display: false,
        },
        ticks: {
          maxRotation: 45,
          minRotation: 45,
        },
      },
    },
  };

  const pieOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'right',
        labels: {
          font: {
            size: 12,
            weight: '600',
          },
          padding: 15,
        },
      },
    },
  };

  return (
    <div className="dataset-detail fade-in">
      {/* Summary Cards */}
      <div className="summary-cards">
        <div className="summary-card">
          <div className="summary-icon" style={{ background: 'linear-gradient(135deg, #667eea, #764ba2)' }}>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
          </div>
          <div className="summary-content">
            <span className="summary-label">Total Equipment</span>
            <span className="summary-value">{dataset.total_count}</span>
          </div>
        </div>

        <div className="summary-card">
          <div className="summary-icon" style={{ background: 'linear-gradient(135deg, #10b981, #059669)' }}>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
            </svg>
          </div>
          <div className="summary-content">
            <span className="summary-label">Avg Flowrate</span>
            <span className="summary-value">{dataset.avg_flowrate.toFixed(2)}</span>
          </div>
        </div>

        <div className="summary-card">
          <div className="summary-icon" style={{ background: 'linear-gradient(135deg, #f59e0b, #d97706)' }}>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
          <div className="summary-content">
            <span className="summary-label">Avg Pressure</span>
            <span className="summary-value">{dataset.avg_pressure.toFixed(2)}</span>
          </div>
        </div>

        <div className="summary-card">
          <div className="summary-icon" style={{ background: 'linear-gradient(135deg, #ef4444, #dc2626)' }}>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
          </div>
          <div className="summary-content">
            <span className="summary-label">Avg Temperature</span>
            <span className="summary-value">{dataset.avg_temperature.toFixed(2)}</span>
          </div>
        </div>
      </div>

      {/* Charts */}
      <div className="charts-grid">
        <div className="card chart-card">
          <div className="card-header">Equipment Type Distribution</div>
          <div className="chart-container">
            <Pie data={pieChartData} options={pieOptions} />
          </div>
        </div>

        <div className="card chart-card">
          <div className="card-header">Parameter Comparison (Bar Chart)</div>
          <div className="chart-container">
            <Bar data={barChartData} options={chartOptions} />
          </div>
        </div>

        <div className="card chart-card full-width">
          <div className="card-header">Parameter Trends (Line Chart)</div>
          <div className="chart-container">
            <Line data={lineChartData} options={chartOptions} />
          </div>
        </div>
      </div>

      {/* Data Table */}
      <div className="card">
        <div className="card-header">Equipment Records</div>
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Equipment Name</th>
                <th>Type</th>
                <th>Flowrate</th>
                <th>Pressure</th>
                <th>Temperature</th>
              </tr>
            </thead>
            <tbody>
              {dataset.records.map((record) => (
                <tr key={record.id}>
                  <td>{record.equipment_name}</td>
                  <td>
                    <span className="badge badge-primary">{record.equipment_type}</span>
                  </td>
                  <td>{record.flowrate.toFixed(2)}</td>
                  <td>{record.pressure.toFixed(2)}</td>
                  <td>{record.temperature.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default DatasetDetail;
