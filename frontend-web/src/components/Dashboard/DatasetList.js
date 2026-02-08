import React from 'react';

const DatasetList = ({
  datasets,
  onSelectDataset,
  onDeleteDataset,
  onDownloadReport,
  selectedDatasetId,
}) => {
  if (datasets.length === 0) {
    return (
      <div className="card empty-state fade-in">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" width="64">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
        </svg>
        <h3>No Datasets Yet</h3>
        <p>Upload your first CSV file to get started with data analysis</p>
      </div>
    );
  }

  return (
    <div className="card dataset-list fade-in">
      <div className="card-header">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" width="24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
        </svg>
        Your Datasets ({datasets.length}/5)
      </div>

      <div className="datasets-grid">
        {datasets.map((dataset) => (
          <div
            key={dataset.id}
            className={`dataset-card ${selectedDatasetId === dataset.id ? 'active' : ''}`}
          >
            <div className="dataset-header">
              <div className="dataset-icon">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <div className="dataset-info">
                <h4>{dataset.filename}</h4>
                <p className="dataset-date">
                  {new Date(dataset.uploaded_at).toLocaleString()}
                </p>
              </div>
            </div>

            <div className="dataset-stats">
              <div className="stat-item">
                <span className="stat-label">Equipment</span>
                <span className="stat-value">{dataset.total_count}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Avg Flow</span>
                <span className="stat-value">{dataset.avg_flowrate.toFixed(1)}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Avg Press</span>
                <span className="stat-value">{dataset.avg_pressure.toFixed(1)}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Avg Temp</span>
                <span className="stat-value">{dataset.avg_temperature.toFixed(1)}</span>
              </div>
            </div>

            <div className="dataset-actions">
              <button
                onClick={() => onSelectDataset(dataset.id)}
                className="btn btn-primary btn-sm"
              >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" width="16">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
                View Details
              </button>
              <button
                onClick={() => onDownloadReport(dataset.id)}
                className="btn btn-success btn-sm"
              >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" width="16">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                PDF
              </button>
              <button
                onClick={() => onDeleteDataset(dataset.id)}
                className="btn btn-danger btn-sm"
              >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" width="16">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default DatasetList;
