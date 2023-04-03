import React, { useState } from 'react';
import ApexCharts from 'apexcharts';
import './style/ManagerScreen.css';

const ManagerScreen = () => {
  const [chartType, setChartType] = useState('line');

  const chartOptions = {
    chart: {
      id: 'users-chart',
      toolbar: {
        show: false
      },
      zoom: {
        enabled: false
      }
    },
    xaxis: {
      categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    },
    tooltip: {
      enabled: true,
      shared: true,
      intersect: false,
      y: {
        formatter: function (val) {
          return val + ' users';
        }
      }
    }
  };

  const chartSeries = [
    {
      name: 'Users',
      data: [30, 40, 45, 50, 49, 60, 70, 91, 125, 135, 150, 180]
    },
    {
      name: 'Data Usage',
      data: [10, 12, 15, 20, 22, 25, 28, 30, 35, 38, 40, 45]
    },
    {
      name: 'Revenue',
      data: [500, 700, 900, 1200, 1500, 2000, 2500, 3000, 3500, 4000, 5000, 6000]
    }
  ];

  const handleChartTypeChange = (type) => {
    setChartType(type);
  };

  return (
    <div className="manager-container">
      <h1 className="manager-header">Manager Dashboard</h1>
      <div className="manager-toggle">
        <button className={chartType === 'line' ? 'active' : ''} onClick={() => handleChartTypeChange('line')}>
          Line Chart
        </button>
        <button className={chartType === 'bar' ? 'active' : ''} onClick={() => handleChartTypeChange('bar')}>
          Bar Chart
        </button>
      </div>
      <div className="manager-chart">
        <ApexCharts options={chartOptions} series={chartSeries} type={chartType} height={350} />
      </div>
    </div>
  );
};

export default ManagerScreen;
