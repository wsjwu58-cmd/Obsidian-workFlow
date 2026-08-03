```
#include<bits/stdc++.h>
#include <fstream>
using namespace std;
const int MAX = 100;
const int INF = INT_MAX;
typedef struct {
	int vernum;
	int edgenum;
	int matrix[MAX][MAX];//邻接矩阵
	string position[MAX];
}mmap;
int located(mmap& mymap, string place) {
	int i;
	for (i = 0; i < mymap.vernum; i++) {

		if (mymap.position[i] == place) {
			return i;
		}
	}
	return -1;
}
void initUDG(mmap& mymap, ifstream& infile) {
	string v1, v2;
	int w;
	if (!(infile >> mymap.vernum >> mymap.edgenum)) {
		mymap.vernum = -1; // 特别标记：文件结束
		return;
	}
	for (int i = 0; i < mymap.vernum; i++)
		infile >> mymap.position[i];
	for (int i = 0; i < mymap.vernum; i++)
		for (int j = 0; j < mymap.vernum; j++)
			mymap.matrix[i][j] = INF;
	cout << "请输入一条路径的两个地点和权值" << endl;
	for (int k = 0; k < mymap.edgenum; k++) {
		infile >> v1 >> v2 >> w;
		int i = located(mymap, v1);
		int j = located(mymap, v2);
		if (i == -1 || j == -1) {
			cout << "输入的地点名称有误" << endl;
			cout << "重新输入" << endl;
			k--;
			continue;
		}
		mymap.matrix[i][j] = w;
	}
}
void dijkstra(mmap& mymap, int start, int dist[], int path[]) {
	bool visited[MAX];
	memset(visited, 0, sizeof(visited));
	for (int i = 0; i < mymap.vernum; i++) {
		dist[i] = mymap.matrix[start][i];
		path[i] = (dist[i] == INF || i == start) ? -1 : start;
	}
	dist[start] = 0;
	visited[start] = 1;
	for (int i = 1; i < mymap.vernum; i++) {
		int u = -1, distmin = INF;
		for (int j = 0; j < mymap.vernum; j++) {
			if (!visited[j] && dist[j] < distmin) {
				distmin = dist[j];
				u = j;
			}
		}
		if (u == -1)
			break;
		visited[u] = 1;
		for (int k = 0; k < mymap.vernum; k++) {
			if (!visited[k] && mymap.matrix[u][k] != INF && dist[u] + mymap.matrix[u][k] < dist[k]) {
				dist[k] = dist[u] + mymap.matrix[u][k];
				path[k] = u;
			}
		}

	}
}
void printpath(mmap& mymap, int path[], int start, int end) {
	stack<int> s;
	int current = end;
	while (current != -1) {
		s.push(current);
		current = path[current];
	}
	while (!s.empty()) {
		cout << mymap.position[s.top()];
		s.pop();
		if (!s.empty())
			cout << "-->";
	}
	cout << endl;
}
void findSecondShortestPath(mmap& mymap, int start, int end) {
	int dist[MAX], path[MAX];
	dijkstra(mymap, start, dist, path);
	if (dist[end] == INF) {
		cout << "不存在路径" << endl;
		return;
	}
	vector<pair<int, int>> minedgepath;
	int current = end;
	while (path[current] != -1) {
		minedgepath.push_back(make_pair(path[current], current));
		current = path[current];
	}
	int secondminpath = INF;
	int temp[MAX];
	bool found = false;
	for (int i = 0; i < minedgepath.size(); i++) {
		int u = minedgepath[i].first;
		int v = minedgepath[i].second;
		int edges = mymap.matrix[u][v];
		mymap.matrix[u][v] = INF;
		int tempdist[MAX], temppath[MAX];
		dijkstra(mymap, start, tempdist, temppath);
		if (tempdist[end] != INF && tempdist[end]<secondminpath && tempdist[end]>dist[end]) {
			secondminpath = tempdist[end];
			memcpy(temp, temppath, sizeof(int) * mymap.vernum);
			found = true;
		}
		mymap.matrix[u][v] = edges;
	}
	if (!found)
		cout << "没有次短路径" << endl;
	else {
		cout << "次短路径长度为" << secondminpath << endl;
		cout << "次短路径为" << endl;
		printpath(mymap, temp, start, end);
	}
	
}
int main() {
	ifstream infile("C:\\Users\\HUAWEI\\Desktop\\plugins\\new 1.txt"); // 打开输入文件

	if (!infile.is_open()) {  
		cout << "无法打开输入文件！" << endl;
		return 0;
	}
	mmap schoolmap;
	int flag;
	string startposition, endposition;
	cout << "*******************  校园导航系统  **********************" << endl;
	cout << "*                                                       *" << endl;
	cout << "*                                                       *" << endl;
	cout << "*                      1.进入                           *" << endl;
	cout << "*                      2.退出                           *" << endl;
	cout << "*                                                       *" << endl;
	cout << "*                                                       *" << endl;
	cout << "*********************************************************" << endl;
	while (true) {
		cout << "请输入选项" << endl;
		cin >> flag;
		if (flag == 1) {
			system("cls");
			initUDG(schoolmap, infile);
			if (schoolmap.vernum == -1) {
				cout << "文件已读完，没有更多数据了！" << endl;
				break;
			}
			cout << "请输入起点和终点的名称:" << endl;;
			infile >> startposition >> endposition;
			int start = located(schoolmap, startposition);
			int end = located(schoolmap, endposition);
			while (start == -1 || end == -1) {
				cout << "请重新输入起点和终点名称:" << endl;
				infile >> startposition >> endposition;
				start = located(schoolmap, startposition);
				end = located(schoolmap, endposition);
			}
			int dist[MAX], path[MAX];
			dijkstra(schoolmap, start, dist, path);
			if (dist[end] == INF) {
				cout << "从" << startposition << "到" << endposition << "无路径" << endl;
			}
			else {
				cout << "从" << startposition << "到" << endposition << "路径长度为" << dist[end] << endl;
				printpath(schoolmap, path, start, end);
				findSecondShortestPath(schoolmap, start, end);
				cout << endl;
			}

		}
		else if (flag == 2)
			break;
		else {
			cout << "没有这个选项" << endl;
		}
	}
	infile.close();
	return 0;
}
```

```
#include <iostream>
#include <stack>
using namespace std;

const int INF = 1000000000;

// 边表节点
struct EdgeNode {
    int to;             // 边的终点
    int weight;        // 边权重
    EdgeNode* next;    // 指向下一个邻接边
};

//顶点信息
struct Vertex {
    string name;      // 顶点（地点）名稱
    EdgeNode* first;   // 第一条邻接边
};

const int MAXN = 100;

// 图的数据结构
struct Graph {
    int n;              // 顶点数
    int m;              // 边数
    Vertex vertices[MAXN];
};

void addEdge(Graph &g, int u, int v, int w) {
    EdgeNode* newEdge = new EdgeNode;
    newEdge->to = v;
    newEdge->weight = w;
    newEdge->next = g.vertices[u].first;
    g.vertices[u].first = newEdge;
}

void dijkstra(Graph &g, int start, int dist[], int prev[]) {
    bool visited[MAXN] = {false};

    for (int i = 0; i < g.n; i++) {
        dist[i] = INF;
        prev[i] = -1;
    }
    dist[start] = 0;

    for (int i = 0; i < g.n; i++) {
        int u = -1;
        int minDist = INF;

        for (int j = 0; j < g.n; j++) {
            if (!visited[j] && dist[j] < minDist) {
                u = j;
                minDist = dist[j];
            }
        }

        if (u == -1) break;

        visited[u] = true;

        for (EdgeNode* p = g.vertices[u].first; p; p = p->next) {
            int v = p->to;
            int w = p->weight;

            if (!visited[v] && dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                prev[v] = u;
            }
        }
    }
}

void printPath(Graph &g, int prev[], int start, int end) {
    stack<int> s;
    int current = end;

    while (current != -1) {
        s.push(current);
        current = prev[current];
    }

    while (!s.empty()) {
        int u = s.top();
        s.pop();

        cout << g.vertices[u].name;
        if (!s.empty()) cout << " -> "; // 不是最后一个时输出箭头
    }
    cout << endl;
}

int main()
{
    Graph g;

    cout << "请输入顶点数和边数: "; 
    cin >> g.n >> g.m;
    cin.ignore();

    cout << "请输入每个顶点的名称:\n";

    for (int i = 0; i < g.n; i++) {
        getline(cin, g.vertices[i].name);
        g.vertices[i].first = NULL;
    }

    cout << "请输入每条有向边信息（起点 终点 权重)：\n";

    for (int i = 0; i < g.m; i++) {
        string from, to;
        int w;
        cin >> from >> to >> w;

        int u = -1, v = -1;

        for (int j = 0; j < g.n; j++) {
            if (g.vertices[j].name == from) u = j;
            if (g.vertices[j].name == to) v = j;
        }

        addEdge(g, u, v, w);
    }

    cout << "请输入起点和终点: "; 
    string startName, endName;
    cin >> startName >> endName;

    int start = -1, end = -1;

    for (int j = 0; j < g.n; j++) {
        if (g.vertices[j].name == startName) start = j;
        if (g.vertices[j].name == endName) end = j;
    }

    int dist[MAXN];
    int prev[MAXN];
    dijkstra(g, start, dist, prev);

    if (dist[end] == INF) {
        cout << "从 " << startName << "到 " << endName << "无法到达" << endl;
    } else {
        cout << "从 " << startName << "到 " << endName << " 的最短距离为: " << dist[end] << endl;
        cout << "最短路径为: "; 
        printPath(g, prev, start, end);
    }

    return 0;
}

```

```
#include<bits/stdc++.h>
#include <fstream>
using namespace std;
const int MAX = 100;
const int INF = INT_MAX;
typedef struct {
	int vernum;
	int edgenum;
	int matrix[MAX][MAX];//邻接矩阵
	string position[MAX];
}mmap;
int located(mmap& mymap, string place) {
	int i;
	for (i = 0; i < mymap.vernum; i++) {
		if (mymap.position[i] == place) {
			return i;
		}
	}
	return -1;
}
void initUDG(mmap& mymap,ifstream&infile) {
	string v1, v2;
	int w;
	if (!(infile >> mymap.vernum >> mymap.edgenum)) {
		mymap.vernum = -1; // 特别标记：文件结束
		return;
	}
	for (int i = 0; i < mymap.vernum; i++)
		infile >> mymap.position[i];
	for (int i = 0; i < mymap.vernum; i++)
		for (int j = 0; j < mymap.vernum; j++)
			mymap.matrix[i][j] = INF;
	cout << "请输入一条路径的两个地点和权值" << endl;
	for (int k = 0; k < mymap.edgenum; k++) {
		infile >> v1 >> v2 >> w;
		int i = located(mymap, v1);
		int j = located(mymap, v2);
		if (i == -1 || j == -1) {
			cout << "输入的地点名称有误" << endl;
			cout << "重新输入" << endl;
			k--;
			continue;
		}
		mymap.matrix[i][j] = w;
	}
}
void dijkstra(mmap& mymap, int start, int dist[], int path[]) {
	bool visited[MAX];
	memset(visited, 0, sizeof(visited));
	for (int i = 0; i < mymap.vernum; i++) {
		dist[i] = mymap.matrix[start][i];
		path[i] = (dist[i] == INF || i == start) ? -1 : start;
	}
	dist[start] = 0;
	visited[start] = 1;
	for (int i = 1; i < mymap.vernum; i++) {
		int u = -1, distmin = INF;
		for (int j = 0; j < mymap.vernum; j++) {
			if (!visited[j] && dist[j] < distmin) {
				distmin = dist[j];
				u = j;
			}
		}
		if (u == -1)
			break;
		visited[u] = 1;
		for (int k = 0; k < mymap.vernum; k++) {
			if (!visited[k] && mymap.matrix[u][k] != INF && dist[u] + mymap.matrix[u][k] < dist[k]) {
				dist[k] = dist[u] + mymap.matrix[u][k];
				path[k] = u;
			}
		}

	}
}
void printpath(mmap& mymap, int path[], int start, int end) {
	stack<int> s;
	int current = end;
	while (current != -1) {
		s.push(current);
		current = path[current];
	}
	while (!s.empty()) {
		cout << mymap.position[s.top()];
		s.pop();
		if (!s.empty())
			cout << "-->";
	}
}
int main() {
	ifstream infile("C:\\Users\\HUAWEI\\Desktop\\plugins\\new 1.txt"); // 打开输入文件

	if (!infile.is_open()) {
		cout << "无法打开输入文件！" << endl;
		return 0;
	}
	mmap schoolmap;
	int flag;
	string startposition, endposition;
	cout << "*******************  校园导航系统  **********************" << endl;
	cout << "*                                                       *" << endl;
	cout << "*                                                       *" << endl;
	cout << "*                      1.进入                           *" << endl;
	cout << "*                      2.退出                           *" << endl;
	cout << "*                                                       *" << endl;
	cout << "*                                                       *" << endl;
	cout << "*********************************************************" << endl;
	while (true) {
		cout << "请输入选项" << endl;
		cin >> flag;
		if (flag == 1) {
			system("cls");
			initUDG(schoolmap,infile);
			if (schoolmap.vernum == -1) {
				cout << "文件已读完，没有更多数据了！" << endl;
				break;
			}
			cout << "请输入起点和终点的名称:" << endl;;
			infile >> startposition >> endposition;
			int start = located(schoolmap, startposition);
			int end = located(schoolmap, endposition);
			while (start == -1 || end == -1) {
				cout << "请重新输入起点和终点名称:" << endl;
				infile >> startposition >> endposition;
				start = located(schoolmap, startposition);
				end = located(schoolmap, endposition);
			}
			int dist[MAX], path[MAX];
			dijkstra(schoolmap, start, dist, path);
			if (dist[end] == INF) {
				cout << "从" << startposition << "到" << endposition << "无路径" << endl;
			}
			else {
				cout << "从" << startposition << "到" << endposition << "路径长度为" << dist[end] << endl;
				printpath(schoolmap, path, start, end);
				cout << endl;
			}
			
		}
		else if (flag == 2)
			break;
		else {
			cout << "没有这个选项" << endl;
		}
	}
	infile.close();
	return 0;
}
```

