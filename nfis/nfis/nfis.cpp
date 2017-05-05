#include<iostream>
#include<vector> 
#define TOP 2
#define RIGHT 3
#define BOTTOM 4
#define LEFT 5
#define SINK 0
#define SOURCE 1

using namespace std;
struct node;
struct edge {
	double capacity;
	double flow;
	node *start;
	node *end;
	edge(double c, node *s, node*e) {
		capacity = c;
		flow = 0;
		start = s;
		end = e;
	}
};

struct node {
	double height;
	double exceed;
	int x;
	int y;
	node **in;
	node **out;
	node(double h, double e, int x, int y, int in_n = 6, int out_n = 6) {
		this->height = h;
		this->exceed = e;
		this->x = x;
		this->y = y;
		in = new node*[in_n];
		out = new node*[out_n];
	}
};

class graph {
	vector<node*> main_graph;
	vector<node*> push_stack;
	edge ***edge_table;// the first element is for soure, the last is for sink. don't forget.
	int row;
	int col;
private:
	int get_id(node *x) {
		return col * x->x + x->y;
	}
	void push(node *x) {
		int exceed = 0;
		for (int i = 0; i < 6; i++)
			if (x->height < x->out[i]->height)
				exceed += edge_table[get_id(x) + 1][i]->flow;
		for (int i = 0; i < 6; i++)
			if (x->height > x->out[i]->height) {
				int tmp = this->edge_table[get_id(x) + 1][i]->capacity - this->edge_table[get_id(x) + 1][i]->flow;
				if (exceed > tmp) {

				}

			}
	}
public:
	graph(int m, int n, double *likelihooda, double *likelihoodb, double penalty) {
		row = m;
		col = n;
		edge_table = new edge**[m * n + 2];
		edge_table[0] = new edge*[m * n];
		edge_table[m * n + 1] = new edge*[m * n];
		main_graph.push_back(new node(m * n + 2, 0, -1, -1, 0, m * n));
		node *tmp_sink = new node(0, 0, -1, -1, m * n);
		for (int i = 0; i < m; i++) {
			for (int j = 0; j < n; j++) {
				edge_table[1 + i * n + j] = new edge*[6];

				edge_table[0][i * n + j]->capacity = likelihooda[i * n + j];
				edge_table[1 + i * n + j][SOURCE]->capacity = 0;
				edge_table[m * n + 1][i * n + j]->capacity = 0;
				edge_table[1 + i * n + j][SINK]->capacity = likelihoodb[i * n + j];

				node *tmp = new node(0, 0, j, i);

				main_graph[0]->out[i * n + j] = tmp;
				tmp_sink->in[i * n + j] = tmp;

				tmp->out[SINK] = tmp_sink;
				if (i > 0) {
					edge_table[1 + i * n + j][TOP] = new edge(penalty, tmp, main_graph[(i - 1) * n + j]);
					edge_table[1 + (i - 1) * n + j][BOTTOM] = new edge(penalty, main_graph[(i - 1) * n + j], tmp);

					tmp->out[TOP] = main_graph[(i - 1) * n + j];
					tmp->in[TOP] = main_graph[(i - 1) * n + j];
					main_graph[(i - 1) * n + j]->in[BOTTOM] = tmp;
					main_graph[(i - 1) * n + j]->out[BOTTOM] = tmp;
				}
				if (j > 0) {
					edge_table[1 + i * n + j][LEFT] = new edge(penalty, tmp, main_graph.back());
					edge_table[i * n + j][RIGHT] = new edge(penalty, main_graph.back(), tmp);

					tmp->out[LEFT] = main_graph.back();
					tmp->in[LEFT] = main_graph.back();
					main_graph.back()->in[RIGHT] = tmp;
					main_graph.back()->out[RIGHT] = tmp;
				}
				tmp->in[SOURCE] = main_graph[0];
				tmp->in[SOURCE] = main_graph[0];
				main_graph.push_back(tmp);
			}
		}
		main_graph.push_back(tmp_sink);
	}
	void my_push() {

	}
};

int main() {
	double a = 1.1;
	double b = 1.3;
	double c = 1.4;
	bool cc = (a + b) * c == a * c + b * c;
	return 0;
}