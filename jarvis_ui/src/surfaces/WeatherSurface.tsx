import React from 'react';
import './WeatherSurface.css';
const WeatherSurface: React.FC<{data?: any; onClose: () => void}> = ({ data, onClose }) => (
    <div className="weather-surface">
        <button onClick={onClose} className="task-surface-close">Close</button>
        <h2 className="surface-title">{data?.location || 'Weather'}</h2>
        <div className="weather-main">
            <div className="weather-temp">{data?.temperature}°</div>
            <div className="weather-condition">{data?.condition}</div>
            <div className="weather-details">
                <div>Humidity: {data?.humidity}%</div>
                <div>Wind: {data?.wind_speed} km/h</div>
            </div>
        </div>
    </div>
);
export default WeatherSurface;