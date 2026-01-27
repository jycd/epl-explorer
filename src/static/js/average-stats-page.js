// Average Stats - standalone page

async function loadTeamsForStats() {
    try {
        const response = await fetch(`${API_BASE}/teams`);
        const teams = await response.json();

        const select = document.getElementById('teamSelect');
        select.innerHTML = '<option value="">Select a team...</option>';

        teams.sort().forEach(team => {
            const option = document.createElement('option');
            option.value = team;
            option.textContent = team;
            select.add(option);
        });
        
        // Check URL parameters for team selection
        const urlParams = new URLSearchParams(window.location.search);
        const teamParam = urlParams.get('team');
        if (teamParam && teams.includes(teamParam)) {
            select.value = teamParam;
        }
    } catch (error) {
        console.error('Error loading teams:', error);
        showStatsError('Failed to load teams.');
        throw error;
    }
}

async function loadSeasonsForStats() {
    try {
        const response = await fetch(`${API_BASE}/seasons`);
        const seasons = await response.json();

        const select = document.getElementById('statsSeasonSelect');
        select.innerHTML = '<option value="">Select a season...</option>';

        seasons.forEach(season => {
            const option = document.createElement('option');
            option.value = season;
            option.textContent = `20${season.substring(0, 2)}/20${season.substring(2, 4)}`;
            select.add(option);
        });

        // Check URL parameters for season selection
        const urlParams = new URLSearchParams(window.location.search);
        const seasonParam = urlParams.get('season');
        if (seasonParam && seasons.includes(seasonParam)) {
            select.value = seasonParam;
        } else if (seasons.length > 0) {
            select.value = seasons[0];
        }
    } catch (error) {
        console.error('Error loading seasons:', error);
        showStatsError('Failed to load seasons.');
        throw error;
    }
}

async function loadAverageStatistics() {
    const team = document.getElementById('teamSelect').value;
    const season = document.getElementById('statsSeasonSelect').value;

    // Update URL to reflect the current selections
    const url = new URL(window.location);
    if (team) {
        url.searchParams.set('team', team);
    } else {
        url.searchParams.delete('team');
    }
    if (season) {
        url.searchParams.set('season', season);
    } else {
        url.searchParams.delete('season');
    }
    window.history.replaceState({}, '', url);

    if (!team) {
        showStatsError('Please select a team.');
        return;
    }

    if (!season) {
        showStatsError('Please select a season.');
        return;
    }

    hideStatsError();
    showStatsLoading(true);

    try {
        const response = await fetch(`${API_BASE}/team-average-statistics/${encodeURIComponent(team)}?season=${season}`);

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const stats = await response.json();
        displayAverageStatistics(stats);
        showStatsLoading(false);

    } catch (error) {
        console.error('Error loading average statistics:', error);
        showStatsError('Failed to load average statistics. Please try again.');
        showStatsLoading(false);
    }
}

function displayAverageStatistics(stats) {
    document.getElementById('avgGoalsFor').textContent = stats.average_goals_for_per_match;
    document.getElementById('avgGoalsAgainst').textContent = stats.average_goals_against_per_match;
    document.getElementById('avgFouls').textContent = stats.average_fouls_per_match;
    document.getElementById('avgYellowCards').textContent = stats.average_yellow_cards_per_match;
    document.getElementById('avgRedCards').textContent = stats.average_red_cards_per_match;

    const tbody = document.getElementById('statsDetailBody');
    tbody.innerHTML = `
        <tr>
            <td>Goals For</td>
            <td>${stats.average_goals_for_per_match}</td>
            <td>${stats.total_goals_for}</td>
        </tr>
        <tr>
            <td>Goals Against</td>
            <td>${stats.average_goals_against_per_match}</td>
            <td>${stats.total_goals_against}</td>
        </tr>
        <tr>
            <td>Fouls</td>
            <td>${stats.average_fouls_per_match}</td>
            <td>${stats.total_fouls}</td>
        </tr>
        <tr>
            <td>Yellow Cards</td>
            <td>${stats.average_yellow_cards_per_match}</td>
            <td>${stats.total_yellow_cards}</td>
        </tr>
        <tr>
            <td>Red Cards</td>
            <td>${stats.average_red_cards_per_match}</td>
            <td>${stats.total_red_cards}</td>
        </tr>
        <tr>
            <td><strong>Matches</strong></td>
            <td>-</td>
            <td><strong>${stats.total_matches}</strong></td>
        </tr>
    `;

    document.getElementById('statsContainer').style.display = 'block';
}

function showStatsLoading(show) {
    document.getElementById('statsLoading').style.display = show ? 'block' : 'none';
    document.getElementById('loadStatsBtn').disabled = show;
    if (show) {
        document.getElementById('statsContainer').style.display = 'none';
    }
}

function showStatsError(message) {
    const errorElement = document.getElementById('statsError');
    errorElement.textContent = message;
    errorElement.style.display = 'block';
}

function hideStatsError() {
    document.getElementById('statsError').style.display = 'none';
}

document.addEventListener('DOMContentLoaded', async function() {
    try {
        await loadTeamsForStats();
        await loadSeasonsForStats();
        
        // Auto-load if URL parameters are present
        const urlParams = new URLSearchParams(window.location.search);
        const teamParam = urlParams.get('team');
        const seasonParam = urlParams.get('season');
        if (teamParam && seasonParam) {
            loadAverageStatistics();
        }
    } catch (error) {
        console.error('Error initializing page:', error);
    }
});
