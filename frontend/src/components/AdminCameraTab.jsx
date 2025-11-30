import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';

const API = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const AdminCameraTab = ({ token, isDark, onIdentificationSuccess }) => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const fileInputRef = useRef(null);

  const [cameraActive, setCameraActive] = useState(false);
  const [capturedImage, setCapturedImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [identificationResult, setIdentificationResult] = useState(null);
  const [error, setError] = useState(null);
  const [stream, setStream] = useState(null);
  const [cameraPermission, setCameraPermission] = useState('pending'); // pending, granted, denied
  const [facingMode, setFacingMode] = useState('environment'); // 'environment' (back) or 'user' (front)

  // Request camera access
  const startCamera = async () => {
    setError(null);
    
    // First, set camera to active so video element renders
    setCameraActive(true);
    
    // Wait a tick for DOM to update with video element
    await new Promise(resolve => setTimeout(resolve, 100));
    
    try {
      console.log('📸 Starting camera...');
      
      // Now check if videoRef exists
      if (!videoRef.current) {
        console.error('Video element still not found after DOM update!');
        setError('Camera element initialization failed. Please try again.');
        setCameraActive(false);
        return;
      }

      const constraints = {
        video: { 
          facingMode: facingMode,
          width: { ideal: 1280 }, 
          height: { ideal: 720 }
        },
        audio: false
      };

      console.log('Requesting getUserMedia with constraints:', constraints);
      const mediaStream = await navigator.mediaDevices.getUserMedia(constraints);
      
      console.log('✅ Media stream obtained, tracks:', mediaStream.getTracks().length);
      setStream(mediaStream);
      
      // Assign stream to video element
      videoRef.current.srcObject = mediaStream;
      
      // Wait a tick, then play
      setTimeout(() => {
        if (videoRef.current) {
          console.log('Attempting to play video...');
          videoRef.current.play()
            .then(() => console.log('✅ Video playing'))
            .catch(error => console.error('❌ Play failed:', error));
        }
      }, 50);
      
      setCameraPermission('granted');
      console.log('✅ Camera started successfully');
      
    } catch (err) {
      setCameraActive(false);
      setCameraPermission('denied');
      console.error('❌ Camera error:', err.name, err.message);
      
      if (err.name === 'NotAllowedError') {
        setError('Camera permission denied. Please enable camera in browser settings.');
      } else if (err.name === 'NotFoundError') {
        setError('No camera found on this device.');
      } else if (err.name === 'NotReadableError') {
        setError('Camera is already in use by another application.');
      } else {
        setError('Cannot access camera: ' + err.message);
      }
    }
  };

  // Stop camera
  const stopCamera = () => {
    console.log('Stopping camera...');
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setStream(null);
    }
    setCameraActive(false);
    console.log('✅ Camera stopped');
  };

  // Flip camera between front and back
  const flipCamera = async () => {
    stopCamera();
    // Wait a moment for the camera to fully stop
    await new Promise(resolve => setTimeout(resolve, 300));
    // Toggle facing mode and restart
    setFacingMode(prev => prev === 'environment' ? 'user' : 'environment');
  };

  // Capture image from video
  const captureImage = () => {
    if (videoRef.current && canvasRef.current) {
      const context = canvasRef.current.getContext('2d');
      canvasRef.current.width = videoRef.current.videoWidth;
      canvasRef.current.height = videoRef.current.videoHeight;
      context.drawImage(videoRef.current, 0, 0);
      const imageData = canvasRef.current.toDataURL('image/jpeg', 0.9);
      setCapturedImage(imageData);
      setCameraActive(false);
      stopCamera();
    }
  };

  // Send captured image to backend for identification
  const identifyOrganism = async () => {
    if (!capturedImage) return;

    setLoading(true);
    setError(null);
    try {
      const response = await axios.post(
        `${API}/admin/identify-organism`,
        { image_data: capturedImage },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      if (response.data.success) {
        setIdentificationResult(response.data);
        // Don't auto-switch view - let user review first
      } else {
        setError(response.data.error || 'Identification failed. Please try another image.');
        setCapturedImage(null);
      }
    } catch (err) {
      const errorMsg = err.response?.data?.error || err.message || 'Failed to identify organism';
      setError(errorMsg);
      setCapturedImage(null);
      console.error('Identification error:', err);
    } finally {
      setLoading(false);
    }
  };

  // Handle file upload as fallback
  const handleFileUpload = async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      setCapturedImage(e.target.result);
      setCameraActive(false);
      stopCamera();
    };
    reader.readAsDataURL(file);
  };

  // Confirm identification and pass to form
  const confirmIdentification = () => {
    if (identificationResult && onIdentificationSuccess) {
      // Pass minimal data to AI agent - just the organism name
      // The AI agent will generate all the morphology, physiology, characteristics, etc.
      onIdentificationSuccess({
        name: identificationResult.organism_name,
        scientific_name: identificationResult.scientific_name,
        classification: identificationResult.classification,
        // Don't include morphology, physiology, description - let AI agent generate these
        images: capturedImage ? [capturedImage] : [],  // Include captured image
      });
    }
  };

  // Reset to initial state
  const resetCapture = () => {
    setCapturedImage(null);
    setIdentificationResult(null);
    setError(null);
    setCameraActive(false);
    stopCamera();
  };

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }
    };
  }, [stream]);

  // Auto-restart camera when facingMode changes
  useEffect(() => {
    if (cameraActive) {
      stopCamera();
      // Small delay to ensure camera fully stops before restarting
      const timeout = setTimeout(() => {
        startCamera();
      }, 300);
      return () => clearTimeout(timeout);
    }
  }, [facingMode]);

  return (
    <div className={`max-w-4xl mx-auto ${isDark ? 'bg-gray-800' : 'bg-white'} rounded-lg shadow-lg p-4 sm:p-6`}>
      <h1 className={`text-2xl sm:text-3xl font-bold mb-2 ${isDark ? 'text-white' : 'text-gray-800'}`}>
        📸 Identify Organism by Camera
      </h1>
      <p className={`mb-6 ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
        Take a photo of an organism to identify it automatically using AI
      </p>

      {/* Step 1: Camera Capture */}
      {!capturedImage ? (
        <div className="space-y-4">
          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
              {error}
            </div>
          )}

          {!cameraActive ? (
            <div className="flex flex-col gap-3 sm:flex-row">
              <button
                onClick={startCamera}
                className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-4 rounded-lg transition flex items-center justify-center gap-2"
              >
                <i className="fas fa-camera"></i> Start Camera
              </button>
              <button
                onClick={() => fileInputRef.current?.click()}
                className="flex-1 bg-gray-600 hover:bg-gray-700 text-white font-semibold py-3 px-4 rounded-lg transition flex items-center justify-center gap-2"
              >
                <i className="fas fa-image"></i> Upload Photo
              </button>
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                onChange={handleFileUpload}
                className="hidden"
              />
            </div>
          ) : (
            <div className="space-y-4">
              {/* Video Preview - Responsive sizing */}
              <div className="relative bg-black rounded-lg overflow-hidden" style={{ 
                aspectRatio: '16/9',
              }}>
                <video
                  ref={videoRef}
                  autoPlay
                  playsInline
                  muted
                  style={{ 
                    width: '100%',
                    height: '100%',
                    objectFit: 'cover',
                    backgroundColor: '#000',
                  }}
                />
                {/* Flip Camera Button - Top Right */}
                <button
                  onClick={flipCamera}
                  className="absolute top-4 right-4 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-3 rounded-lg transition flex items-center gap-2 shadow-lg"
                  title="Flip camera"
                >
                  <i className="fas fa-sync-alt"></i> <span className="hidden sm:inline">Flip</span>
                </button>
              </div>

              {/* Capture Buttons - Responsive layout */}
              <div className="flex flex-col gap-2 sm:flex-row">
                <button
                  onClick={captureImage}
                  className="flex-1 bg-green-600 hover:bg-green-700 text-white font-semibold py-3 px-4 rounded-lg transition flex items-center justify-center gap-2"
                >
                  <i className="fas fa-check-circle"></i> Capture Photo
                </button>
                <button
                  onClick={() => stopCamera()}
                  className="flex-1 bg-red-600 hover:bg-red-700 text-white font-semibold py-3 px-4 rounded-lg transition flex items-center justify-center gap-2"
                >
                  <i className="fas fa-times-circle"></i> Cancel
                </button>
              </div>
            </div>
          )}

          {/* Hidden Canvas for image capture */}
          <canvas ref={canvasRef} className="hidden" />
        </div>
      ) : (
        <div className="space-y-4">
          {/* Step 2: Image Preview and Identification */}
          <div className="relative bg-gray-100 rounded-lg overflow-hidden" style={{ aspectRatio: '16/9' }}>
            <img src={capturedImage} alt="Captured" className="w-full h-full object-contain" />
          </div>

          {/* Loading State */}
          {loading && (
            <div className={`p-4 rounded-lg text-center ${isDark ? 'bg-gray-700' : 'bg-gray-100'}`}>
              <div className="flex justify-center mb-2">
                <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-blue-600"></div>
              </div>
              <p className={isDark ? 'text-white' : 'text-gray-800'}>Analyzing image with AI...</p>
            </div>
          )}

          {/* Identification Results */}
          {identificationResult && !loading && (
            <div className={`p-4 rounded-lg border-2 ${isDark ? 'bg-gray-700 border-green-600' : 'bg-green-50 border-green-300'}`}>
              <h3 className={`text-lg font-bold mb-3 flex items-center gap-2 ${isDark ? 'text-green-300' : 'text-green-700'}`}>
                <i className="fas fa-check-circle"></i> Organism Identified
              </h3>

              {/* Main Info Grid - Responsive */}
              <div className="grid grid-cols-1 gap-3 mb-4 sm:grid-cols-2">
                <div>
                  <p className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>Common Name</p>
                  <p className={`text-lg font-semibold ${isDark ? 'text-white' : 'text-gray-800'}`}>
                    {identificationResult.organism_name}
                  </p>
                </div>
                <div>
                  <p className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>Scientific Name</p>
                  <p className={`text-lg font-semibold italic ${isDark ? 'text-white' : 'text-gray-800'}`}>
                    {identificationResult.scientific_name}
                  </p>
                </div>
              </div>

              {/* Confidence Badge - Color coded */}
              <div className="mb-4">
                <p className={`text-sm mb-1 ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>Confidence</p>
                <div className="flex items-center gap-2">
                  <div className="flex-1 bg-gray-300 rounded-full h-2">
                    <div
                      className={`h-2 rounded-full transition-all ${
                        identificationResult.confidence >= 80
                          ? 'bg-green-600'
                          : identificationResult.confidence >= 60
                          ? 'bg-yellow-600'
                          : 'bg-red-600'
                      }`}
                      style={{ width: `${identificationResult.confidence}%` }}
                    />
                  </div>
                  <span className={`font-semibold min-w-12 ${isDark ? 'text-white' : 'text-gray-800'}`}>
                    {identificationResult.confidence}%
                  </span>
                </div>
              </div>

              {/* Description */}
              {identificationResult.description && (
                <div className="mb-4">
                  <p className={`text-sm font-semibold mb-1 ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>
                    Description
                  </p>
                  <p className={`text-sm leading-relaxed ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>
                    {identificationResult.description}
                  </p>
                </div>
              )}

              {/* Characteristics - Responsive tags */}
              {identificationResult.characteristics && identificationResult.characteristics.length > 0 && (
                <div className="mb-4">
                  <p className={`text-sm font-semibold mb-2 ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>
                    Characteristics
                  </p>
                  <div className="flex flex-wrap gap-2">
                    {identificationResult.characteristics.map((char, idx) => (
                      <span
                        key={idx}
                        className={`px-3 py-1 rounded-full text-sm ${
                          isDark ? 'bg-gray-600 text-gray-100' : 'bg-blue-100 text-blue-800'
                        }`}
                      >
                        {char}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Classification Table - Responsive */}
              {identificationResult.classification && (
                <div className="mb-4">
                  <p className={`text-sm font-semibold mb-2 ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>
                    Taxonomy
                  </p>
                  <div className="grid grid-cols-2 gap-2 sm:grid-cols-3 md:grid-cols-4">
                    {Object.entries(identificationResult.classification).map(([key, value]) => (
                      <div key={key} className={`p-2 rounded ${isDark ? 'bg-gray-600' : 'bg-gray-100'}`}>
                        <p className={`text-xs uppercase font-semibold ${isDark ? 'text-gray-300' : 'text-gray-600'}`}>
                          {key}
                        </p>
                        <p className={`text-sm ${isDark ? 'text-white' : 'text-gray-800'}`}>{value}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Error State - Retake Photo */}
          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
              {error}
            </div>
          )}

          {/* Action Buttons - Responsive layout */}
          {!loading && (
            <div className="flex flex-col gap-2 sm:flex-row">
              {identificationResult && (
                <button
                  onClick={confirmIdentification}
                  className="flex-1 bg-green-600 hover:bg-green-700 text-white font-semibold py-3 px-4 rounded-lg transition flex items-center justify-center gap-2"
                >
                  <i className="fas fa-check"></i> Yes, Add This Organism
                </button>
              )}
              <button
                onClick={resetCapture}
                className={`flex-1 ${
                  identificationResult
                    ? 'bg-gray-600 hover:bg-gray-700'
                    : 'bg-blue-600 hover:bg-blue-700'
                } text-white font-semibold py-3 px-4 rounded-lg transition flex items-center justify-center gap-2`}
              >
                <i className="fas fa-redo"></i> {identificationResult ? 'Try Another Photo' : 'Back'}
              </button>
            </div>
          )}

          {/* Identify Button - If image not yet identified */}
          {!identificationResult && !loading && (
            <button
              onClick={identifyOrganism}
              className="w-full bg-purple-600 hover:bg-purple-700 text-white font-semibold py-3 px-4 rounded-lg transition flex items-center justify-center gap-2"
            >
              <i className="fas fa-search"></i> Identify This Organism
            </button>
          )}
        </div>
      )}
    </div>
  );
};

export default AdminCameraTab;
