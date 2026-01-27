let chartInstance = null;
let winRateChartInstance = null;
let standingChartInstance = null;

async function loadTeams() {
    try {
        const response = await fetch('/api/teams');
        const teams = await response.json();
        const select = document.getElementById('teamSelect');
        select.innerHTML = '';
        
        if (teams.length === 0) {
            const option = document.createElement('option');
            option.text = "No teams found";
            select.add(option);
            return;
        }

        teams.forEach(team => {
            const option = document.createElement('option');
            option.value = team;
            option.text = team;
            select.add(option);
        });
        
        // Select the first team by default and fetch data
        const urlParams = new URLSearchParams(window.location.search);
        const teamParam = urlParams.get('team');

        if (teamParam && teams.includes(teamParam)) {
            select.value = teamParam;
            fetchData();
        } else if (teams.length > 0) {
            select.value = teams[0];
            // Update URL to reflect the default selection
            const url = new URL(window.location);
            url.searchParams.set('team', teams[0]);
            window.history.replaceState({}, '', url);
            fetchData();
        }

    } catch (error) {
        console.error('Error loading teams:', error);
        document.getElementById('error-message').innerText = 'Failed to load teams.';
    }
}

async function fetchData() {
    const team = document.getElementById('teamSelect').value;
    const errorDiv = document.getElementById('error-message');
    const button = document.getElementById('fetchButton');
    
    // Update URL to reflect the current team selection
    const url = new URL(window.location);
    url.searchParams.set('team', team);
    window.history.replaceState({}, '', url);
    
    if (!team) {
        errorDiv.innerText = 'Please select a club.';
        return;
    }

    errorDiv.innerText = '';
    button.disabled = true;
    button.innerHTML = '<span class="loading-spinner"></span>Loading...';

    // Show skeleton loaders for charts
    showChartLoading(true);

    try {
        // Fetch Team History
        const historyResponse = await fetch(`/api/team-history/${encodeURIComponent(team)}`);
        if (!historyResponse.ok) {
            throw new Error(`Failed to fetch history data (${historyResponse.status})`);
        }
        const historyData = await historyResponse.json();
        
        // Fetch Standing History
        const standingResponse = await fetch(`/api/team-standing-history/${encodeURIComponent(team)}`);
        if (!standingResponse.ok) {
            throw new Error(`Failed to fetch standing data (${standingResponse.status})`);
        }
        const standingData = await standingResponse.json();

        if (historyData.length === 0) {
            errorDiv.innerText = `No history data found for ${team}.`;
            destroyAllCharts();
            return;
        }

        if (standingData.length === 0) {
            errorDiv.innerText = `No standing data found for ${team}.`;
            destroyAllCharts();
            return;
        }

        // The API returns data from newest to oldest
        historyData.reverse(); 
        standingData.reverse();

        const labels = historyData.map(d => {
            const s = d.season;
            return `20${s.substring(0, 2)}/${s.substring(2, 4)}`;
        });
        
        const gdValues = historyData.map(d => d.goal_difference);
        const goalsFor = historyData.map(d => d.goals_for);
        const goalsAgainst = historyData.map(d => d.goals_against);
        
        const winRates = historyData.map(d => d.win_rate);
        const drawRates = historyData.map(d => d.draw_rate);
        const lossRates = historyData.map(d => d.loss_rate);
        
        const wins = historyData.map(d => d.wins);
        const draws = historyData.map(d => d.draws);
        const losses = historyData.map(d => d.losses);

        const standingLabels = standingData.map(d => {
            const s = d.season;
            return `20${s.substring(0, 2)}/${s.substring(2, 4)}`;
        });
        const standings = standingData.map(d => d.position);
        const fullStandings = standingData.map(d => d.full_standings);

        renderStandingChart(team, standingLabels, standings, fullStandings);
        renderWinRateChart(team, labels, winRates, drawRates, lossRates, wins, draws, losses);
        renderGdChart(team, labels, gdValues, goalsFor, goalsAgainst);

    } catch (error) {
        console.error('Error:', error);
        if (error.message.includes('404')) {
            errorDiv.innerText = 'Team not found. Please select a valid team.';
        } else if (error.message.includes('500')) {
            errorDiv.innerText = 'Server error. Please try again later.';
        } else {
            errorDiv.innerText = 'Network error. Please check your connection and try again.';
        }
        destroyAllCharts();
    } finally {
        button.disabled = false;
        button.innerHTML = 'Show Chart';
        showChartLoading(false);
    }
}

function showChartLoading(show) {
    const standingLoading = document.getElementById('standingLoading');
    const winRateLoading = document.getElementById('winRateLoading');
    const gdLoading = document.getElementById('gdLoading');
    
    if (show) {
        standingLoading.style.display = 'flex';
        winRateLoading.style.display = 'flex';
        gdLoading.style.display = 'flex';
    } else {
        standingLoading.style.display = 'none';
        winRateLoading.style.display = 'none';
        gdLoading.style.display = 'none';
    }
}

function destroyAllCharts() {
    if (chartInstance) chartInstance.destroy();
    if (winRateChartInstance) winRateChartInstance.destroy();
    if (standingChartInstance) standingChartInstance.destroy();
}

function renderStandingChart(team, labels, data, fullStandings) {
    const ctx = document.getElementById('standingChart').getContext('2d');
    
    if (standingChartInstance) {
        standingChartInstance.destroy();
    }

    standingChartInstance = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'League Position',
                    data: data,
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    tension: 0.3,
                    fill: true,
                    pointRadius: 6,
                    pointHoverRadius: 8,
                    pointBackgroundColor: '#667eea',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    borderWidth: 3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        reverse: true,
                        min: 1,
                        max: 20,
                        ticks: {
                            stepSize: 1,
                            font: {
                                size: 12,
                                weight: '500'
                            }
                        },
                        title: {
                            display: true,
                            text: 'Position',
                            font: {
                                size: 14,
                                weight: '600'
                            }
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Season',
                            font: {
                                size: 14,
                                weight: '600'
                            }
                        },
                        grid: {
                            display: false
                        }
                    }
                },
                plugins: {
                    title: {
                        display: true,
                        text: `League Standing History - ${team}`,
                        font: {
                            size: 18,
                            weight: '700'
                        },
                        padding: 20
                    },
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleFont: {
                            size: 14,
                            weight: '600'
                        },
                        bodyFont: {
                            size: 12
                        },
                        padding: 12,
                        cornerRadius: 8,
                        callbacks: {
                            afterBody: function(context) {
                                const index = context[0].dataIndex;
                                const standings = fullStandings[index];
                                return standings;
                            }
                        }
                    }
                }
            }
        });
}

function renderWinRateChart(team, labels, winRates, drawRates, lossRates, wins, draws, losses) {
    const ctx = document.getElementById('winRateChart').getContext('2d');
    
    if (winRateChartInstance) {
        winRateChartInstance.destroy();
    }

    winRateChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Win Rate (%)',
                    data: winRates,
                    borderColor: '#22c55e',
                    backgroundColor: 'rgba(34, 197, 94, 0.1)',
                    tension: 0.3,
                    fill: true,
                    pointRadius: 5,
                    pointHoverRadius: 7,
                    borderWidth: 3
                },
                {
                    label: 'Draw Rate (%)',
                    data: drawRates,
                    borderColor: '#fbbf24',
                    backgroundColor: 'rgba(251, 191, 36, 0.1)',
                    tension: 0.3,
                    fill: true,
                    pointRadius: 5,
                    pointHoverRadius: 7,
                    borderWidth: 3
                },
                {
                    label: 'Loss Rate (%)',
                    data: lossRates,
                    borderColor: '#f87171',
                    backgroundColor: 'rgba(248, 113, 113, 0.1)',
                    tension: 0.3,
                    fill: true,
                    pointRadius: 5,
                    pointHoverRadius: 7,
                    borderWidth: 3
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        font: {
                            size: 12,
                            weight: '500'
                        }
                    },
                    title: {
                        display: true,
                        text: 'Percentage (%)',
                        font: {
                            size: 14,
                            weight: '600'
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Season',
                        font: {
                            size: 14,
                            weight: '600'
                        }
                    },
                    grid: {
                        display: false
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: `Win/Draw/Loss Rate History - ${team}`,
                    font: {
                        size: 18,
                        weight: '700'
                    },
                    padding: 20
                },
                legend: {
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 15,
                        font: {
                            size: 12,
                            weight: '500'
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleFont: {
                        size: 14,
                        weight: '600'
                    },
                    bodyFont: {
                        size: 12
                    },
                    padding: 12,
                    cornerRadius: 8,
                    callbacks: {
                        afterLabel: function(context) {
                            const index = context.dataIndex;
                            const datasetLabel = context.dataset.label;
                            if (datasetLabel.includes('Win')) {
                                return `Wins: ${wins[index]}`;
                            } else if (datasetLabel.includes('Draw')) {
                                return `Draws: ${draws[index]}`;
                            } else if (datasetLabel.includes('Loss')) {
                                return `Losses: ${losses[index]}`;
                            }
                            return '';
                        }
                    }
                }
            }
        }
    });
}

function renderGdChart(team, labels, values, goalsFor, goalsAgainst) {
    const ctx = document.getElementById('gdChart').getContext('2d');
    
    if (chartInstance) {
        chartInstance.destroy();
    }

    chartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: `${team} Goal Difference`,
                data: values.map(v => Math.abs(v) < 0.5 ? 0.8 : v), // Give near-zero values a minimum height for hoverability
                backgroundColor: values.map(v => {
                    if (Math.abs(v) < 0.5) return 'rgba(102, 126, 234, 0.9)';
                    if (v > 0) return 'rgba(16, 185, 129, 0.8)';
                    return 'rgba(239, 68, 68, 0.8)';
                }),
                borderColor: values.map(v => {
                    if (Math.abs(v) < 0.5) return '#667eea';
                    if (v > 0) return '#10b981';
                    return '#ef4444';
                }),
                borderWidth: 2,
                borderRadius: 8,
                borderSkipped: false,
                barPercentage: 0.7
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        font: {
                            size: 12,
                            weight: '500'
                        }
                    },
                    title: {
                        display: true,
                        text: 'Goal Difference',
                        font: {
                            size: 14,
                            weight: '600'
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Season',
                        font: {
                            size: 14,
                            weight: '600'
                        }
                    },
                    grid: {
                        display: false
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: `Goal Difference History - ${team}`,
                    font: {
                        size: 18,
                        weight: '700'
                    },
                    padding: 20
                },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.9)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    borderColor: '#667eea',
                    borderWidth: 1,
                    cornerRadius: 8,
                    padding: 12,
                    callbacks: {
                        label: function(context) {
                            const index = context.dataIndex;
                            const originalValue = values[index]; // Use original values array
                            const season = labels[index];
                            const gf = goalsFor[index];
                            const ga = goalsAgainst[index];
                            const displayValue = Math.abs(originalValue) < 0.5 ? '0' : originalValue;
                            return [
                                `${season}`,
                                `GD: ${displayValue}`,
                                `GF: ${gf} | GA: ${ga}`
                            ];
                        }
                    }
                }
            }
        }
    });
}

// Load teams on page load
document.addEventListener('DOMContentLoaded', loadTeams);
