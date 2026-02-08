import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { datasetAPI } from '../../services/api';
import UploadSection from './UploadSection';
import DatasetList from './DatasetList';
import DatasetDetail from './DatasetDetail';
import './Dashboard.css';

const Dashboard = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [datasets, setDatasets] = useState([]);
  const [selectedDataset, setSelectedDataset] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDatasets();
  }, []);

  const fetchDatasets = async () => {
    try {
      setLoading(true);
      const response = await datasetAPI.getDatasets();
      setDatasets(response.data);
      setError('');
    } catch (err) {
      setError('Failed to fetch datasets');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleUploadSuccess = () => {
    fetchDatasets();
    setSelectedDataset(null);
  };

  const handleSelectDataset = async (datasetId) => {
    try {
      const response = await datasetAPI.getDatasetDetail(datasetId);
      setSelectedDataset(response.data);
    } catch (err) {
      setError('Failed to fetch dataset details');
      console.error(err);
    }
  };

  const handleDeleteDataset = async (datasetId) => {
    if (window.confirm('Are you sure you want to delete this dataset?')) {
      try {
        await datasetAPI.deleteDataset(datasetId);
        fetchDatasets();
        if (selectedDataset?.id === datasetId) {
          setSelectedDataset(null);
        }
      } catch (err) {
        setError('Failed to delete dataset');
        console.error(err);
      }
    }
  };

  const handleDownloadReport = async (datasetId) => {
    try {
      const response = await datasetAPI.downloadReport(datasetId);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `report_${datasetId}_${Date.now()}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      setError('Failed to download report');
      console.error(err);
    }
  };

  return (
    <div className="dashboard">
      {/* Navigation Header */}
      <header className="dashboard-header">
        <div className="header-content">
          <div className="header-left">
            <div className="header-icon">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <div>
              <h1>Chemical Equipment Visualizer</h1>
              <p>Data Analysis & Visualization Platform</p>
            </div>
          </div>
          <div className="header-right">
            <div className="user-info">
              <div className="user-avatar" onClick={() => navigate('/profile')} style={{ cursor: 'pointer' }}>
                {user?.first_name?.[0] || user?.username?.[0]?.toUpperCase()}
              </div>
              <div className="user-details">
                <span className="user-name">
                  {user?.first_name} {user?.last_name || user?.username}
                </span>
                <span className="user-email">{user?.email}</span>
              </div>
            </div>
            <button onClick={() => navigate('/profile')} className="btn btn-outline">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" width="20">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              Profile
            </button>
            <button onClick={logout} className="btn btn-secondary">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" width="20">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              Logout
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="dashboard-main">
        <div className="dashboard-container">
          {error && (
            <div className="alert alert-error">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" width="20">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              {error}
            </div>
          )}

          {/* Upload Section */}
          <UploadSection onUploadSuccess={handleUploadSuccess} />

          {/* Dataset List */}
          {loading ? (
            <div className="loading-container">
              <div className="spinner"></div>
              <p>Loading datasets...</p>
            </div>
          ) : (
            <>
              <DatasetList
                datasets={datasets}
                onSelectDataset={handleSelectDataset}
                onDeleteDataset={handleDeleteDataset}
                onDownloadReport={handleDownloadReport}
                selectedDatasetId={selectedDataset?.id}
              />

              {/* Dataset Detail */}
              {selectedDataset && (
                <DatasetDetail dataset={selectedDataset} />
              )}
            </>
          )}
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
