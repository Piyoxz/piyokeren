import axios from 'axios';

const API_BASE_URL = '/api';

export const getCvs = async (userId) => {
    const response = await axios.get(`${API_BASE_URL}/get_cvs`, {
        params: { userId }
    });
    return response.data.cvs;
};

// Function to get a specific CV by its id
export const getCvById = async (cvId) => {
    const response = await axios.get(`${API_BASE_URL}/get_cv/${cvId}`);
    return response.data.cv;
};

export const saveCv = async (cvData) => {
    const response = await axios.post(`${API_BASE_URL}/add_cv`, cvData);
    return response.data.message;
};

export const getPositions = async () => {
    const response = await axios.get(`${API_BASE_URL}/positions`);
    return response.data.positions;
};

export const getPhrasesByPosition = async (position) => {
    const response = await axios.get(`${API_BASE_URL}/position_phrases`, { params: { position } });
    return response.data.phrases;
};

export const getEducationalLevels = async () => {
    const response = await axios.get(`${API_BASE_URL}/educational_levels`);
    return response.data.levels;
};

export const getFieldsByLevel = async (level) => {
    const response = await axios.get(`${API_BASE_URL}/fields`, { params: { level } });
    return response.data.fields;
};

export const getPhrasesByField = async (level, field) => {
    const response = await axios.get(`${API_BASE_URL}/field_phrases`, { params: { level, field } });
    return response.data.phrases;
};

export const daftarPiyomyid = async (userData) => {
    const response = await axios.post(`${API_BASE_URL}/add_user`, userData);
    return response.data.message;
};

export const updateDataCv = async (data) => {
    const response = await axios.post(`${API_BASE_URL}/update_cv`, data);
    return response.data.message;
};

export const generateCv = async (data) => {
    const response = await axios.post(`${API_BASE_URL}/generate_cv`, data);
    return response.data;
};

export const deleteCv = async (cvId) => {
    const response = await axios.delete(`${API_BASE_URL}/delete_cv/${cvId}`);
    return response.data.message;
};
