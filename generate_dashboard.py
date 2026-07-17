import json
import os
import sys

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CBSE Class 12 Physics Intelligence Platform</title>
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- jQuery and DataTables -->
    <script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
    <link rel="stylesheet" href="https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css">
    <script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>
    
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    
    <style>
        body { font-family: 'Inter', sans-serif; background-color: #f8fafc; color: #1e293b; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        .nav-tab.active { border-bottom: 2px solid #2563eb; color: #2563eb; font-weight: 600; }
        .dataTables_wrapper .dataTables_length select { padding-right: 2rem; }
    </style>
</head>
<body class="antialiased">

<nav class="bg-white shadow-sm sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
            <div class="flex items-center">
                <svg class="h-8 w-8 text-blue-600 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                <span class="font-bold text-xl text-slate-800">Physics Intelligence</span>
            </div>
            <div class="flex space-x-8">
                <button class="nav-tab active inline-flex items-center px-1 pt-1 text-sm font-medium text-slate-500 hover:text-slate-700" onclick="switchTab('overview')">Overview</button>
                <button class="nav-tab inline-flex items-center px-1 pt-1 text-sm font-medium text-slate-500 hover:text-slate-700" onclick="switchTab('priority')">Priority Matrix</button>
                <button class="nav-tab inline-flex items-center px-1 pt-1 text-sm font-medium text-slate-500 hover:text-slate-700" onclick="switchTab('clusters')">Clusters</button>
                <button class="nav-tab inline-flex items-center px-1 pt-1 text-sm font-medium text-slate-500 hover:text-slate-700" onclick="switchTab('database')">Question Database</button>
            </div>
        </div>
    </div>
</nav>

<main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

    <!-- Overview Tab -->
    <div id="overview" class="tab-content active space-y-6">
        <div class="bg-white rounded-lg shadow px-6 py-8">
            <h2 class="text-2xl font-bold text-slate-800 mb-4">Executive Summary</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6" id="summaryCards">
                <!-- Summary cards injected via JS -->
            </div>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="bg-white rounded-lg shadow px-6 py-6">
                <h3 class="text-lg font-semibold text-slate-800 mb-4">Topic Frequency Distribution</h3>
                <canvas id="topicFreqChart"></canvas>
            </div>
            <div class="bg-white rounded-lg shadow px-6 py-6">
                <h3 class="text-lg font-semibold text-slate-800 mb-4">Significant Topic Flags</h3>
                <div id="significantTopics" class="space-y-4"></div>
            </div>
        </div>
    </div>

    <!-- Priority Matrix Tab -->
    <div id="priority" class="tab-content">
        <div class="bg-white rounded-lg shadow px-6 py-8">
            <h2 class="text-2xl font-bold text-slate-800 mb-6">Topic Priority Matrix</h2>
            <div class="overflow-x-auto">
                <table id="matrixTable" class="w-full text-sm text-left">
                    <thead class="text-xs text-slate-500 uppercase bg-slate-50">
                        <tr>
                            <th class="px-4 py-3">Rank</th>
                            <th class="px-4 py-3">Topic Code</th>
                            <th class="px-4 py-3">Topic Name</th>
                            <th class="px-4 py-3">Priority Score</th>
                            <th class="px-4 py-3">Frequency</th>
                            <th class="px-4 py-3">Compartment Bias</th>
                            <th class="px-4 py-3">Flags</th>
                        </tr>
                    </thead>
                    <tbody id="matrixBody"></tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- Clusters Tab -->
    <div id="clusters" class="tab-content">
        <div class="bg-white rounded-lg shadow px-6 py-8">
            <h2 class="text-2xl font-bold text-slate-800 mb-6">Semantic Question Clusters</h2>
            <p class="text-sm text-slate-500 mb-6">Identifies repeating concepts across different sets, years, and paper types.</p>
            <table id="dtClusters" class="display w-full text-sm text-left">
                <thead class="text-xs text-slate-500 uppercase bg-slate-50">
                    <tr>
                        <th>Topic</th>
                        <th>Concept Representation</th>
                        <th>Variants</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody></tbody>
            </table>
        </div>
    </div>

    <!-- Database Tab -->
    <div id="database" class="tab-content">
        <div class="bg-white rounded-lg shadow px-6 py-8">
            <h2 class="text-2xl font-bold text-slate-800 mb-6">Raw Question Database</h2>
            <table id="dtQuestions" class="display w-full text-sm text-left">
                <thead class="text-xs text-slate-500 uppercase bg-slate-50">
                    <tr>
                        <th class="w-full py-3 px-4">Question Details</th>
                        <th>Year</th>
                        <th>Type</th>
                        <th>Topic</th>
                        <th>Text</th>
                    </tr>
                </thead>
                <tbody></tbody>
            </table>
        </div>
    </div>

</main>

<!-- Modal for Variants -->
<div id="clusterModal" class="hidden fixed inset-0 bg-slate-900 bg-opacity-50 overflow-y-auto h-full w-full z-50">
    <div class="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white">
        <div class="flex justify-between items-center pb-3 border-b">
            <h3 class="text-xl font-bold text-slate-800" id="modalTitle">Cluster Variants</h3>
            <button onclick="closeModal()" class="text-slate-400 hover:text-slate-600">
                <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
            </button>
        </div>
        <div class="mt-4">
            <p class="text-sm text-slate-500 font-semibold mb-2">Base Concept:</p>
            <p class="text-md text-slate-800 bg-slate-50 p-3 rounded mb-4" id="modalConcept"></p>
            <p class="text-sm text-slate-500 font-semibold mb-2">Variants Found:</p>
            <ul class="space-y-3 max-h-96 overflow-y-auto" id="modalVariants"></ul>
        </div>
    </div>
</div>

<script>
    // JSON DATA INJECTION
    const INJECTED_DATA = {json_payload};

    // Tab Switching
    function switchTab(tabId) {
        document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
        document.querySelectorAll('.nav-tab').forEach(el => el.classList.remove('active'));
        
        document.getElementById(tabId).classList.add('active');
        event.currentTarget.classList.add('active');
    }

    // Render Overview
    function renderOverview() {
        const meta = INJECTED_DATA.metadata;
        const qCount = INJECTED_DATA.questions.length;
        const cCount = INJECTED_DATA.clusters.filter(c => c.variantCount > 1).length;
        
        document.getElementById('summaryCards').innerHTML = `
            <div class="bg-blue-50 p-4 rounded-lg border border-blue-100">
                <p class="text-sm text-blue-600 font-semibold">Total Papers Analyzed</p>
                <p class="text-3xl font-bold text-blue-900">${meta.totalPapersProcessed || 0}</p>
            </div>
            <div class="bg-emerald-50 p-4 rounded-lg border border-emerald-100">
                <p class="text-sm text-emerald-600 font-semibold">Clean Questions Extracted</p>
                <p class="text-3xl font-bold text-emerald-900">${qCount}</p>
            </div>
            <div class="bg-purple-50 p-4 rounded-lg border border-purple-100">
                <p class="text-sm text-purple-600 font-semibold">Repeating Clusters Found</p>
                <p class="text-3xl font-bold text-purple-900">${cCount}</p>
            </div>
        `;

        // Chart
        const intel = INJECTED_DATA.intelligence.topics;
        let sortedTopics = Object.values(intel).sort((a, b) => b.priorityScore - a.priorityScore);
        
        new Chart(document.getElementById('topicFreqChart'), {
            type: 'bar',
            data: {
                labels: sortedTopics.slice(0,10).map(t => t.topicName.substring(0,20) + '...'),
                datasets: [{
                    label: 'Priority Score',
                    data: sortedTopics.slice(0,10).map(t => t.priorityScore.toFixed(1)),
                    backgroundColor: '#3b82f6',
                    borderRadius: 4
                }]
            }
        });

        // Flags
        let flagsHtml = '';
        sortedTopics.forEach(t => {
            let flags = [];
            const st = t.statisticalTests;
            if(st.chiSquare && st.chiSquare.significant) flags.push('<span class="bg-red-100 text-red-800 px-2 py-1 rounded text-xs font-semibold">Compartment Bias</span>');
            if(st.mannWhitneyU && st.mannWhitneyU.significant) flags.push('<span class="bg-orange-100 text-orange-800 px-2 py-1 rounded text-xs font-semibold">Mark Variance</span>');
            if(st.zTest && st.zTest.significant) flags.push('<span class="bg-indigo-100 text-indigo-800 px-2 py-1 rounded text-xs font-semibold">Derivation Heavy</span>');
            
            if(flags.length > 0) {
                flagsHtml += `
                    <div class="flex justify-between items-center p-3 bg-slate-50 rounded border border-slate-100">
                        <span class="font-medium text-sm">${t.topicName}</span>
                        <div class="space-x-2">${flags.join('')}</div>
                    </div>`;
            }
        });
        if(!flagsHtml) flagsHtml = '<p class="text-slate-500">No significant flags detected.</p>';
        document.getElementById('significantTopics').innerHTML = flagsHtml;
    }

    // Render Matrix Table
    function renderMatrix() {
        const intel = INJECTED_DATA.intelligence.topics;
        let sorted = Object.values(intel).sort((a,b) => b.priorityScore - a.priorityScore);
        
        let html = '';
        sorted.forEach((t, i) => {
            let flags = [];
            if(t.statisticalTests.chiSquare && t.statisticalTests.chiSquare.significant) flags.push('Comp Bias');
            if(t.statisticalTests.zTest && t.statisticalTests.zTest.significant) flags.push('Derivations');
            
            html += `
                <tr class="border-b">
                    <td class="px-4 py-3 font-semibold">${i+1}</td>
                    <td class="px-4 py-3 text-slate-500">${t.code}</td>
                    <td class="px-4 py-3 font-medium">${t.topicName}</td>
                    <td class="px-4 py-3 text-blue-600 font-bold">${t.priorityScore.toFixed(1)}</td>
                    <td class="px-4 py-3">${t.rawMetrics.frequency}</td>
                    <td class="px-4 py-3">${(t.rawMetrics.compartmentBias*100).toFixed(1)}%</td>
                    <td class="px-4 py-3 text-xs text-red-500">${flags.join(', ')}</td>
                </tr>
            `;
        });
        document.getElementById('matrixBody').innerHTML = html;
    }

    window.sortedClusters = [];
    
    $(document).ready(function() {
        // Init DataTables for Questions
        $('#dtQuestions').DataTable({
            data: INJECTED_DATA.questions.filter(q => q.topicCode !== '00'),
            columns: [
                { 
                    data: null,
                    render: function(data, type, row) {
                        return `
                            <div class="p-5 bg-white border border-slate-200 rounded-lg shadow-sm hover:shadow-md transition-shadow my-2 w-full">
                                <div class="flex flex-wrap gap-2 mb-3">
                                    <span class="bg-blue-100 text-blue-800 text-xs font-semibold px-2.5 py-1 rounded">${row.topicName}</span>
                                    <span class="bg-slate-100 text-slate-800 text-xs font-medium px-2.5 py-1 rounded border border-slate-300">${row.year} ${row.paperType}</span>
                                    <span class="bg-emerald-100 text-emerald-800 text-xs font-medium px-2.5 py-1 rounded">${row.marks ? row.marks + ' Marks' : 'Unknown Marks'}</span>
                                    <span class="bg-purple-100 text-purple-800 text-xs font-medium px-2.5 py-1 rounded">Set ${row.setNumber}</span>
                                </div>
                                <p class="text-slate-800 text-base leading-relaxed whitespace-pre-wrap font-medium">${row.questionText}</p>
                            </div>
                        `;
                    }
                },
                { data: 'year', visible: false },
                { data: 'paperType', visible: false },
                { data: 'topicName', visible: false },
                { data: 'questionText', visible: false }
            ],
            pageLength: 10,
            order: [[1, "desc"]],
            language: {
                search: "Search Questions:"
            }
        });

        // Init DataTables for Clusters
        const clusters = INJECTED_DATA.clusters.filter(c => c.variantCount > 1);
        window.sortedClusters = clusters;
        
        $('#dtClusters').DataTable({
            data: clusters,
            columns: [
                { data: 'topicName' },
                { 
                    data: 'conceptLabel',
                    render: function(data, type, row) {
                        return data.length > 100 ? data.substring(0, 100) + '...' : data;
                    }
                },
                { data: 'variantCount' },
                { 
                    data: null,
                    render: function(data, type, row, meta) {
                        return `<button onclick="openModal(${meta.row})" class="bg-blue-100 hover:bg-blue-200 text-blue-700 py-1 px-3 rounded text-xs font-semibold">View Variants</button>`;
                    }
                }
            ],
            order: [[2, "desc"]]
        });

        renderOverview();
        renderMatrix();
    });

    // Modal logic
    window.openModal = function(idx) {
        const c = window.sortedClusters[idx];
        document.getElementById('modalTitle').innerText = c.topicName + ' Variants';
        document.getElementById('modalConcept').innerText = c.conceptLabel;
        
        let html = '';
        c.variants.forEach(v => {
            html += `
                <li class="p-3 border rounded border-slate-200">
                    <span class="inline-block bg-slate-100 text-slate-600 text-xs px-2 py-1 rounded mb-2">
                        ${v.year} | ${v.paperType} | Set ${v.setNumber} | ${v.marks ? v.marks+'M' : 'Unknown M'}
                    </span>
                    <p class="text-sm text-slate-800">${v.questionText}</p>
                </li>
            `;
        });
        document.getElementById('modalVariants').innerHTML = html;
        document.getElementById('clusterModal').classList.remove('hidden');
    }

    window.closeModal = function() {
        document.getElementById('clusterModal').classList.add('hidden');
    }
</script>

</body>
</html>"""

def main():
    try:
        with open('physics_questions_database.json', 'r') as f:
            db = json.load(f)
        with open('question_clusters.json', 'r') as f:
            clusters = json.load(f)
        with open('question_intelligence.json', 'r') as f:
            intelligence = json.load(f)
    except Exception as e:
        print(f"Error loading JSON data: {e}")
        sys.exit(1)

    payload = {
        "metadata": db.get("metadata", {}),
        "questions": db.get("questions", []),
        "clusters": clusters,
        "intelligence": intelligence
    }

    # Minify the payload to save space
    payload_str = json.dumps(payload, separators=(',', ':'))
    
    html_output = HTML_TEMPLATE.replace("{json_payload}", payload_str)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_output)
        
    print("Successfully generated index.html")

if __name__ == "__main__":
    main()
