import React from 'react';
import { useAuth } from '../../context/AuthContext';
import './Profile.css';

const Profile = () => {
  const { user } = useAuth();

  const getYear = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).getFullYear();
  };

  return (
    <div className="profile-page">
      <div className="profile-body">
        <div className="profile-tab-content">
          <div className="info-section fade-in">
            <h2 className="section-title">Account Information</h2>
            <div className="info-grid">
              <div className="info-item">
                <label className="info-label">Username</label>
                <div className="info-value">{user?.username}</div>
              </div>
              <div className="info-item">
                <label className="info-label">Email Address</label>
                <div className="info-value">{user?.email}</div>
              </div>
              <div className="info-item">
                <label className="info-label">First Name</label>
                <div className="info-value">{user?.first_name || 'Not set'}</div>
              </div>
              <div className="info-item">
                <label className="info-label">Last Name</label>
                <div className="info-value">{user?.last_name || 'Not set'}</div>
              </div>
              <div className="info-item">
                <label className="info-label">Member Since</label>
                <div className="info-value">{getYear(user?.date_joined)}</div>
              </div>
              <div className="info-item">
                <label className="info-label">Account Status</label>
                <div className="info-value">
                  <span className="status-badge active">Active</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;
