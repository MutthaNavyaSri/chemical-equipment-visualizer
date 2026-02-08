import React, { useState } from 'react';
import { datasetAPI } from '../../services/api';

const UploadSection = ({ onUploadSuccess }) => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      if (!selectedFile.name.endsWith('.csv')) {
        setError('Please select a CSV file');
        setFile(null);
        return;
      }
      setFile(selectedFile);
      setError('');
      setSuccess('');
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file first');
      return;
    }

    setUploading(true);
    setError('');
    setSuccess('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      await datasetAPI.uploadCSV(formData);
      setSuccess('File uploaded successfully!');
      setFile(null);
      // Reset file input
      document.getElementById('csv-upload').value = '';
      onUploadSuccess();
    } catch (err) {
      setError(
        err.response?.data?.error || 
        'Failed to upload file. Please check the format and try again.'
      );
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="card upload-section fade-in">
      <div className="card-header">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" width="24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
        </svg>
        Upload CSV Data
      </div>

      {error && (
        <div className="alert alert-error">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" width="20">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          {error}
        </div>
      )}

      {success && (
        <div className="alert alert-success">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" width="20">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          {success}
        </div>
      )}

      <div className="upload-area">
        <div className="file-input-wrapper">
          <input
            type="file"
            id="csv-upload"
            accept=".csv"
            onChange={handleFileChange}
            className="file-input"
          />
          <label htmlFor="csv-upload" className="file-label">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" width="48">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <span>{file ? file.name : 'Click to select CSV file'}</span>
            <span className="file-info">
              {file ? `Size: ${(file.size / 1024).toFixed(2)} KB` : 'Required columns: Equipment Name, Type, Flowrate, Pressure, Temperature'}
            </span>
          </label>
        </div>

        <button
          onClick={handleUpload}
          className="btn btn-primary"
          disabled={!file || uploading}
        >
          {uploading ? (
            <>
              <div className="spinner" style={{ width: '20px', height: '20px', borderWidth: '2px' }}></div>
              Uploading...
            </>
          ) : (
            <>
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" width="20">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
              </svg>
              Upload & Analyze
            </>
          )}
        </button>
      </div>

      <div className="upload-info">
        <div className="info-item">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" width="20">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span>Up to 5 datasets are stored per user</span>
        </div>
        <div className="info-item">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" width="20">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span>Automatic analysis and visualization</span>
        </div>
      </div>
    </div>
  );
};

export default UploadSection;
