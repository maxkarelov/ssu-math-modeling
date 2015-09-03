#include <iostream>
#include <fstream>

using namespace std;

void task1(float V, float a, float b, int n, float eps);

int main() {

	ofstream out("output.txt");

	float a, b, eps = 1e-6;
	int n;

	cout << "Enter n: ";
	cin >> n;

	return 0;
}

void task1(float V, float a, float b, int n, float eps) {

	vector<float> v1, v2;
	vector<int> v3;
	
	for (float x = a; x <= b; x += abs(b - a) / n) {

		v1.push_back(x);

		int i, j;
		
		float summand = 0;
		float sum = 0;
		float d = 1;

		for (i = 0, j = 1; summand >= eps; i++, j += 2) {

			summand = pow(-1, i) * pow(V * x, j) / d;
			
			if (summand < eps) {
				v2.push_back(sum);
				v3.push_back(i);

				break;

			} else {
				sum += summand;
			}

			d *= (j + 1 * j + 2);
		}
	}
}