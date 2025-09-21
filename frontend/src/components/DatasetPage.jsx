import React, { useEffect, useState } from 'react';
import { Upload, Database, FileText, Loader2, CheckCircle, AlertCircle } from 'lucide-react';
import { api } from '../api';

export default function DatasetPage() {
  const [list, setList] = useState([]);
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [note, setNote] = useState('');

  async function fetchList() {
    setNote('');
    setLoading(true);
    const client = api();

    try {
      console.log('Attempting to fetch from /datasets');
      const res = await client.get('/datasets');
      console.log('Response from /datasets:', res.data);
      setList(dedupe(res.data?.datasets || res.data || []));
      setLoading(false);
      return;
    } catch (e) {
      console.log('Failed to fetch from /datasets, trying /datasets/list:', e);
    }
    
    try {
      const res = await client.get('/datasets/list');
      console.log('Response from /datasets/list:', res.data);
      setList(dedupe(res.data?.datasets || res.data || []));
    } catch (e2) {
      console.error('Both endpoints failed:', e2);
      setNote('Failed to load datasets. Make sure the backend exposes /datasets or /datasets/list.');
    } finally {
      setLoading(false);
    }
  }

  function dedupe(arr) {
    const seen = new Set();
    return (arr || []).filter(item => {
      const key = String(item.id || item.dataset_id || item.name || Math.random());
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });
  }

  useEffect(() => { fetchList(); }, []);

  async function upload(e) {
    e.preventDefault();
    if (!file) {
      setNote('Please select a file first.');
      return;
    }
    
    console.log('Starting upload for file:', file.name, 'Size:', file.size);
    setLoading(true);
    setNote('Uploading...');
    
    const client = api();
    
    console.log('Available API methods:', Object.getOwnPropertyNames(client));
    
    try {
      const form = new FormData();
      form.append('file', file);
      
      console.log('FormData contents:');
      for (let pair of form.entries()) {
        console.log(pair[0] + ':', pair[1]);
      }
      console.log('File details:', {
        name: file.name,
        size: file.size,
        type: file.type,
        lastModified: file.lastModified
      });
      
      console.log('FormData created, making request to /datasets/upload');
      
      const client = api();
      const baseURL = client.defaults?.baseURL || client.baseURL || '';
      console.log('Base URL:', baseURL);
      
      let response, result;
      
      if (baseURL) {
        const fullURL = baseURL + '/datasets/upload';
        console.log('Trying fetch with URL:', fullURL);
        
        response = await fetch(fullURL, {
          method: 'POST',
          body: form
        });
        
        if (!response.ok) {
          const errorText = await response.text();
          console.error('Fetch response error:', errorText);
          throw new Error(`HTTP ${response.status}: ${errorText}`);
        }
        
        result = await response.json();
      } else {
        console.log('No base URL found, trying API client...');
        response = await client.post('/datasets/upload', form);
        result = response.data || response;
      }
      
      console.log('Upload response:', result);
      
      setNote('Upload successful.');
      setFile(null);
      
      const fileInput = document.querySelector('input[type="file"]');
      if (fileInput) fileInput.value = '';
      
      if (result.dataset?.name || result.dataset?.id) {
        setNote(`Upload successful: ${result.dataset.name || result.dataset.id}`);
      }
      
      await fetchList();
      
    } catch (e) {
      console.error('Upload failed:', e);
      
      if (e.response) {
        console.error('Error response status:', e.response.status);
        console.error('Error response data:', e.response.data);
        console.error('Error response headers:', e.response.headers);
        
        let errorMsg = `Upload failed: ${e.response.status} ${e.response.statusText}`;
        if (e.response.data?.detail) {
          errorMsg += ` - ${JSON.stringify(e.response.data.detail)}`;
        } else if (e.response.data?.message) {
          errorMsg += ` - ${e.response.data.message}`;
        } else if (typeof e.response.data === 'string') {
          errorMsg += ` - ${e.response.data}`;
        }
        setNote(errorMsg);
      } else if (e.request) {
        console.error('No response received:', e.request);
        setNote('Upload failed: No response from server. Check if the backend is running.');
      } else {
        console.error('Request setup error:', e.message);
        setNote(`Upload failed: ${e.message}`);
      }
    } finally {
      setLoading(false);
    }
  }

  const isError = note.includes('failed') || note.includes('Failed');
  const isSuccess = note.includes('successful') || note.includes('Upload successful');

  return (
    <div className="min-h-screen bg-gradient-to-br from-violet-50 via-purple-50 to-indigo-100 p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex justify-center items-center gap-3 mb-4">
            <div className="p-3 bg-gradient-to-r from-violet-600 to-indigo-600 rounded-2xl shadow-lg">
              <Database className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-violet-600 to-indigo-600 bg-clip-text text-transparent">
              Dataset Management
            </h1>
          </div>
          <p className="text-gray-600 text-lg">Upload, manage, and explore your datasets with ease</p>
        </div>

        {/* Upload Section */}
        <div className="bg-white/80 backdrop-blur-sm rounded-3xl shadow-xl border border-white/50 p-8 mb-8 hover:shadow-2xl transition-all duration-300">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-gradient-to-r from-emerald-500 to-teal-500 rounded-xl">
              <Upload className="w-6 h-6 text-white" />
            </div>
            <h2 className="text-2xl font-bold text-gray-800">Upload New Dataset</h2>
          </div>
          
          <div className="space-y-4">
            <div className="relative">
              <input 
                type="file" 
                className="block w-full text-sm text-gray-600 file:mr-4 file:py-3 file:px-6 file:rounded-xl file:border-0 file:text-sm file:font-semibold file:bg-gradient-to-r file:from-violet-500 file:to-purple-500 file:text-white hover:file:from-violet-600 hover:file:to-purple-600 file:transition-all file:duration-200 file:shadow-md hover:file:shadow-lg cursor-pointer bg-gray-50 border-2 border-dashed border-gray-200 rounded-2xl p-4 hover:border-violet-300 transition-colors"
                onChange={e => setFile(e.target.files[0])}
                accept=".csv,.parquet,.feather,.xlsx,.xls"
              />
            </div>
            
            <button 
              className={`w-full py-4 px-6 rounded-2xl font-semibold text-white transition-all duration-200 flex items-center justify-center gap-2 ${
                loading || !file 
                  ? 'bg-gray-400 cursor-not-allowed' 
                  : 'bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-700 hover:to-purple-700 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5'
              }`}
              onClick={upload}
              disabled={loading || !file}
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Uploading...
                </>
              ) : (
                <>
                  <Upload className="w-5 h-5" />
                  Upload Dataset
                </>
              )}
            </button>
          </div>

          {note && (
            <div className={`mt-4 p-4 rounded-2xl flex items-center gap-3 ${
              isError 
                ? 'bg-red-50 border border-red-200 text-red-700' 
                : isSuccess 
                ? 'bg-emerald-50 border border-emerald-200 text-emerald-700'
                : 'bg-blue-50 border border-blue-200 text-blue-700'
            }`}>
              {isError ? (
                <AlertCircle className="w-5 h-5 text-red-500" />
              ) : isSuccess ? (
                <CheckCircle className="w-5 h-5 text-emerald-500" />
              ) : (
                <Loader2 className="w-5 h-5 animate-spin text-blue-500" />
              )}
              <span className="text-sm font-medium">{note}</span>
            </div>
          )}
        </div>

        {/* Datasets List */}
        <div className="bg-white/80 backdrop-blur-sm rounded-3xl shadow-xl border border-white/50 p-8 hover:shadow-2xl transition-all duration-300">
          <div className="flex items-center gap-3 mb-8">
            <div className="p-2 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-xl">
              <FileText className="w-6 h-6 text-white" />
            </div>
            <h2 className="text-2xl font-bold text-gray-800">Available Datasets</h2>
          </div>

          {loading ? (
            <div className="flex flex-col items-center justify-center py-16">
              <Loader2 className="w-8 h-8 animate-spin text-violet-600 mb-4" />
              <p className="text-gray-600 font-medium">Loading datasets...</p>
            </div>
          ) : list.length === 0 ? (
            <div className="text-center py-16">
              <div className="w-24 h-24 mx-auto mb-6 bg-gradient-to-r from-gray-100 to-gray-200 rounded-full flex items-center justify-center">
                <Database className="w-12 h-12 text-gray-400" />
              </div>
              <p className="text-gray-500 text-lg font-medium">No datasets found</p>
              <p className="text-gray-400 mt-2">Upload your first dataset to get started</p>
            </div>
          ) : (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {list.map((d, idx) => (
                <div 
                  key={d.id || d.dataset_id || idx} 
                  className="group bg-gradient-to-br from-white to-gray-50 p-6 rounded-2xl border border-gray-100 hover:border-violet-200 shadow-md hover:shadow-xl transition-all duration-300 hover:-translate-y-1"
                >
                  <div className="flex items-start justify-between mb-4">
                    <div className="p-2 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-xl group-hover:from-indigo-600 group-hover:to-purple-600 transition-all duration-200">
                      <FileText className="w-5 h-5 text-white" />
                    </div>
                  </div>
                  
                  <h3 className="font-bold text-gray-800 text-lg mb-2 group-hover:text-violet-700 transition-colors">
                    {d.name || `Dataset ${d.id || d.dataset_id}`}
                  </h3>
                  
                  <div className="space-y-2">
                    <div className="text-sm text-gray-500">
                      <span className="font-medium">ID:</span> {d.id || d.dataset_id}
                    </div>
                    {(d.rows || d.row_count) && (
                      <div className="flex items-center gap-2">
                        <div className="w-2 h-2 bg-emerald-500 rounded-full"></div>
                        <span className="text-sm text-gray-600 font-medium">
                          {(d.rows || d.row_count).toLocaleString()} rows
                        </span>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}