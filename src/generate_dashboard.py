import json
import os

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Physics AI Extraction Platform</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; background-color: #0f172a; color: #f8fafc; }
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: #1e293b; }
        ::-webkit-scrollbar-thumb { background: #475569; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #64748b; }
    </style>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        brand: { 500: '#3b82f6', 600: '#2563eb' }
                    }
                }
            }
        }
    </script>
</head>
<body class="antialiased h-screen flex overflow-hidden">
    <!-- INJECT_DATA -->

    <div x-data="appData()" class="flex h-full w-full">
        
        <!-- Sidebar -->
        <aside class="w-64 bg-slate-900 border-r border-slate-800 flex flex-col transition-all">
            <div class="p-6">
                <div class="flex items-center gap-3">
                    <div class="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center font-bold text-lg">AI</div>
                    <span class="font-bold text-xl tracking-tight text-white">ExtractionDB</span>
                </div>
                <p class="text-xs text-slate-400 mt-2">v2.0 Data Pipeline</p>
            </div>
            
            <nav class="flex-1 px-4 space-y-2 mt-4">
                <a @click="currentTab = 'overview'" :class="currentTab === 'overview' ? 'bg-blue-600/10 text-blue-400 border-blue-500' : 'text-slate-400 hover:bg-slate-800 hover:text-white border-transparent'" class="flex items-center gap-3 px-4 py-3 rounded-lg cursor-pointer border-l-2 transition-colors">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"></path></svg>
                    <span class="font-medium">Overview</span>
                </a>
                <a @click="currentTab = 'questions'" :class="currentTab === 'questions' ? 'bg-blue-600/10 text-blue-400 border-blue-500' : 'text-slate-400 hover:bg-slate-800 hover:text-white border-transparent'" class="flex items-center gap-3 px-4 py-3 rounded-lg cursor-pointer border-l-2 transition-colors">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"></path></svg>
                    <span class="font-medium">Questions DB</span>
                </a>
                <a @click="currentTab = 'clusters'" :class="currentTab === 'clusters' ? 'bg-blue-600/10 text-blue-400 border-blue-500' : 'text-slate-400 hover:bg-slate-800 hover:text-white border-transparent'" class="flex items-center gap-3 px-4 py-3 rounded-lg cursor-pointer border-l-2 transition-colors">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path></svg>
                    <span class="font-medium">Concept Clusters</span>
                </a>
            </nav>
        </aside>

        <!-- Main Content -->
        <main class="flex-1 flex flex-col overflow-hidden bg-slate-950">
            <!-- Header -->
            <header class="h-16 border-b border-slate-800 bg-slate-900/50 backdrop-blur flex items-center px-8 shrink-0">
                <h1 class="text-lg font-semibold text-white capitalize" x-text="currentTab.replace('-', ' ')"></h1>
            </header>
            
            <div class="flex-1 overflow-y-auto p-8 relative">
                
                <!-- Overview Tab -->
                <div x-show="currentTab === 'overview'" x-transition.opacity>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                        <div class="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-sm hover:border-slate-700 transition">
                            <h3 class="text-slate-400 text-sm font-medium uppercase tracking-wider mb-2">Papers Processed</h3>
                            <p class="text-4xl font-light text-white" x-text="metadata.totalPapersProcessed"></p>
                        </div>
                        <div class="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-sm hover:border-slate-700 transition">
                            <h3 class="text-slate-400 text-sm font-medium uppercase tracking-wider mb-2">Total Questions</h3>
                            <p class="text-4xl font-light text-white" x-text="questions.length"></p>
                        </div>
                        <div class="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-sm hover:border-slate-700 transition">
                            <h3 class="text-slate-400 text-sm font-medium uppercase tracking-wider mb-2">Repeated Concepts</h3>
                            <p class="text-4xl font-light text-white" x-text="clusters.filter(c => c.variantCount > 1).length"></p>
                        </div>
                    </div>
                    
                    <h2 class="text-xl font-semibold mb-4 text-white">Topics Intelligence Matrix</h2>
                    <div class="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
                        <table class="w-full text-left border-collapse">
                            <thead>
                                <tr class="bg-slate-800/50 border-b border-slate-800">
                                    <th class="px-6 py-4 text-xs font-semibold text-slate-400 uppercase tracking-wider">Topic</th>
                                    <th class="px-6 py-4 text-xs font-semibold text-slate-400 uppercase tracking-wider">Priority Score</th>
                                    <th class="px-6 py-4 text-xs font-semibold text-slate-400 uppercase tracking-wider">Freq</th>
                                    <th class="px-6 py-4 text-xs font-semibold text-slate-400 uppercase tracking-wider">Comp Bias</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-slate-800/50">
                                <template x-for="topic in sortedTopics" :key="topic.code">
                                    <tr class="hover:bg-slate-800/30 transition-colors">
                                        <td class="px-6 py-4 font-medium text-slate-200" x-text="topic.topicName"></td>
                                        <td class="px-6 py-4 text-blue-400 font-bold" x-text="topic.priorityScore.toFixed(1)"></td>
                                        <td class="px-6 py-4 text-slate-400" x-text="topic.rawMetrics.frequency"></td>
                                        <td class="px-6 py-4 text-slate-400">
                                            <span x-text="(topic.rawMetrics.compartmentBias*100).toFixed(1) + '%'"></span>
                                        </td>
                                    </tr>
                                </template>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- Questions DB Tab -->
                <div x-show="currentTab === 'questions'" x-transition.opacity>
                    <div class="flex flex-col md:flex-row gap-4 mb-6">
                        <input x-model="searchQuery" type="text" placeholder="Search questions..." class="flex-1 bg-slate-900 border border-slate-700 text-white rounded-lg px-4 py-3 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition shadow-sm placeholder-slate-500">
                        
                        <select x-model="filterTopic" class="bg-slate-900 border border-slate-700 text-white rounded-lg px-4 py-3 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 shadow-sm appearance-none">
                            <option value="">All Topics</option>
                            <template x-for="topic in uniqueTopics">
                                <option :value="topic" x-text="topic"></option>
                            </template>
                        </select>
                    </div>
                    
                    <div class="text-sm text-slate-400 mb-4 font-medium tracking-wide">
                        Showing <span x-text="filteredQuestions.length" class="text-white"></span> questions
                    </div>
                    
                    <div class="space-y-4">
                        <template x-for="q in paginatedQuestions" :key="q.id">
                            <div class="bg-slate-900 border border-slate-800 rounded-xl p-6 hover:border-slate-700 transition shadow-sm group">
                                <div class="flex flex-wrap gap-2 mb-4">
                                    <span class="bg-blue-500/10 text-blue-400 border border-blue-500/20 text-xs font-semibold px-2.5 py-1 rounded-full" x-text="q.topicName"></span>
                                    <span class="bg-slate-800 text-slate-300 border border-slate-700 text-xs font-medium px-2.5 py-1 rounded-full" x-text="q.year + ' ' + q.paperType"></span>
                                    <span class="bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs font-medium px-2.5 py-1 rounded-full" x-text="q.marks ? q.marks + ' Marks' : 'Unknown Marks'"></span>
                                    <span class="bg-purple-500/10 text-purple-400 border border-purple-500/20 text-xs font-medium px-2.5 py-1 rounded-full" x-text="'Set ' + q.setNumber"></span>
                                </div>
                                <p class="text-slate-200 text-base leading-relaxed whitespace-pre-wrap font-medium" x-text="q.questionText"></p>
                            </div>
                        </template>
                    </div>
                    
                    <!-- Pagination -->
                    <div class="mt-8 flex justify-between items-center bg-slate-900 border border-slate-800 rounded-lg p-2" x-show="filteredQuestions.length > itemsPerPage">
                        <button @click="prevPage()" :disabled="currentPage === 1" class="px-4 py-2 bg-slate-800 text-white rounded hover:bg-slate-700 disabled:opacity-50 transition text-sm font-medium">Previous</button>
                        <span class="text-slate-400 text-sm">Page <span x-text="currentPage" class="text-white font-semibold"></span> of <span x-text="totalPages" class="text-white font-semibold"></span></span>
                        <button @click="nextPage()" :disabled="currentPage === totalPages" class="px-4 py-2 bg-slate-800 text-white rounded hover:bg-slate-700 disabled:opacity-50 transition text-sm font-medium">Next</button>
                    </div>
                </div>

                <!-- Clusters Tab -->
                <div x-show="currentTab === 'clusters'" x-transition.opacity>
                    <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                        <template x-for="c in repeatedClusters" :key="c.topicCode + Math.random()">
                            <div class="bg-slate-900 border border-slate-800 rounded-xl p-6 hover:border-slate-700 transition flex flex-col">
                                <div class="flex justify-between items-start mb-4">
                                    <span class="bg-blue-500/10 text-blue-400 text-xs font-semibold px-2.5 py-1 rounded-full border border-blue-500/20" x-text="c.topicName"></span>
                                    <span class="flex items-center justify-center w-8 h-8 rounded-full bg-slate-800 text-slate-300 font-bold text-sm border border-slate-700" x-text="c.variantCount"></span>
                                </div>
                                <p class="text-slate-200 font-medium text-sm mb-6 flex-1" x-text="c.conceptLabel.substring(0, 120) + (c.conceptLabel.length > 120 ? '...' : '')"></p>
                                <button @click="openCluster(c)" class="w-full bg-slate-800 hover:bg-blue-600 text-white py-2.5 rounded-lg text-sm font-medium transition-colors">View Variants</button>
                            </div>
                        </template>
                    </div>
                </div>
            </div>
        </main>
        
        <!-- Cluster Modal -->
        <div x-show="activeCluster" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm" x-transition.opacity style="display: none;">
            <div @click.away="activeCluster = null" class="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-3xl max-h-[85vh] flex flex-col shadow-2xl">
                <div class="p-6 border-b border-slate-800 flex justify-between items-start">
                    <div>
                        <span class="text-blue-400 text-xs font-bold uppercase tracking-wider mb-2 block" x-text="activeCluster?.topicName"></span>
                        <h3 class="text-lg font-medium text-white" x-text="activeCluster?.conceptLabel"></h3>
                    </div>
                    <button @click="activeCluster = null" class="text-slate-400 hover:text-white bg-slate-800 rounded-full p-2 transition shrink-0 ml-4">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                    </button>
                </div>
                <div class="p-6 overflow-y-auto space-y-4">
                    <template x-for="(v, i) in activeCluster?.variants" :key="i">
                        <div class="bg-slate-800/50 border border-slate-700/50 p-4 rounded-xl">
                            <div class="flex gap-2 mb-2">
                                <span class="bg-slate-700 text-slate-300 text-xs px-2 py-1 rounded" x-text="v.year + ' ' + v.paperType"></span>
                                <span class="bg-emerald-500/20 text-emerald-400 text-xs px-2 py-1 rounded" x-text="v.marks ? v.marks+'M' : 'Unknown M'"></span>
                            </div>
                            <p class="text-slate-200 text-sm" x-text="v.questionText"></p>
                        </div>
                    </template>
                </div>
            </div>
        </div>
    </div>

    <script>
        function appData() {
            return {
                currentTab: 'questions',
                searchQuery: '',
                filterTopic: '',
                currentPage: 1,
                itemsPerPage: 50,
                activeCluster: null,
                
                questions: window.INJECTED_DATA.questions.filter(q => q.topicCode !== '00' && q.questionText.trim().length > 0),
                metadata: window.INJECTED_DATA.metadata,
                intelligence: window.INJECTED_DATA.intelligence,
                clusters: window.INJECTED_DATA.clusters,
                
                get sortedTopics() {
                    return Object.values(this.intelligence.topics)
                        .sort((a,b) => b.priorityScore - a.priorityScore);
                },
                
                get uniqueTopics() {
                    const topics = new Set(this.questions.map(q => q.topicName));
                    return Array.from(topics).sort();
                },
                
                get filteredQuestions() {
                    return this.questions.filter(q => {
                        const matchesSearch = q.questionText.toLowerCase().includes(this.searchQuery.toLowerCase());
                        const matchesTopic = this.filterTopic === '' || q.topicName === this.filterTopic;
                        return matchesSearch && matchesTopic;
                    });
                },
                
                get totalPages() {
                    return Math.ceil(this.filteredQuestions.length / this.itemsPerPage) || 1;
                },
                
                get paginatedQuestions() {
                    const start = (this.currentPage - 1) * this.itemsPerPage;
                    const end = start + this.itemsPerPage;
                    return this.filteredQuestions.slice(start, end);
                },
                
                get repeatedClusters() {
                    return this.clusters.filter(c => c.variantCount > 1)
                        .sort((a,b) => b.variantCount - a.variantCount);
                },
                
                nextPage() {
                    if (this.currentPage < this.totalPages) this.currentPage++;
                },
                
                prevPage() {
                    if (this.currentPage > 1) this.currentPage--;
                },
                
                openCluster(cluster) {
                    this.activeCluster = cluster;
                }
            }
        }
        
        // Reset pagination when filters change
        document.addEventListener('alpine:init', () => {
            Alpine.effect(() => {
                const search = Alpine.store('searchQuery');
                const filter = Alpine.store('filterTopic');
                // Could implement watchers here, but x-model binds handle it cleanly enough
            })
        });
    </script>
</body>
</html>
"""

def generate_dashboard():
    with open("physics_questions_database.json", "r") as f:
        db = json.load(f)
        
    with open("question_intelligence.json", "r") as f:
        intelligence = json.load(f)
        
    with open("question_clusters.json", "r") as f:
        clusters = json.load(f)
        
    injected_data = {
        "metadata": db["metadata"],
        "questions": db["questions"],
        "intelligence": intelligence,
        "clusters": clusters
    }
    
    script_tag = f"""
    <script>
        window.INJECTED_DATA = {json.dumps(injected_data)};
    </script>
    """
    
    html = HTML_TEMPLATE.replace("<!-- INJECT_DATA -->", script_tag)
    
    with open("index.html", "w") as f:
        f.write(html)
        
    print("Successfully generated stunning index.html")

if __name__ == "__main__":
    generate_dashboard()
