#include <iostream>
#include <fstream>
#include <cmath>
#include "distancias.h"
//#include "Algoritmos.h"
#include "FileOp.h"

using namespace std;

int main(int argc, char ** argv){

	if(argc != 4){
		cout<<"Faltan argumentos <valsFile> <namesFile> <pelis>"<<endl;
		return 0;
	}
	string valsFileName(argv[1]);
	string namesFileName(argv[2]);
	string pelisFileName(argv[3]);
	vector<string> names = getBdNames(namesFileName);
	vector<ValVec> vals = getBdVals(valsFileName, names.size());
	vector<string> pelis = getBdNames(pelisFileName);



	//Print

	for(string s : names) cout<<s<<"\t";
	cout<<endl;
	for(int i = 0; i < vals.size(); i++){
		for(int j = 0; j < vals.front().size(); j++){
			cout<<vals[j][i]<<"\t";
			if(j == 0) cout<<"\t";
		}
		cout<<endl;
	}

	//End Print
	while(true){
		for(int i = 0; i < names.size(); i++){
			cout<<i<<") "<<names[i]<<endl;
		}

		cout<<"1 Distancia Manhattan"<<endl;
		cout<<"2 Distancia Euclidiana"<<endl;
		cout<<"3 Distancia Minkowski"<<endl;
		cout<<"4 Distancia Coseno"<<endl;
		cout<<"5 Aproximacion de Person"<<endl;


		int option = 0;
		cout<<"Opcion->";
		cin>>option;

		int a = 0;
		int b = 0;
		int k = 0;
    cout<<"Entre quines?? (indices)"<<endl;
		cout<<"A->";
		cin>>a;
		cout<<"B->";
		cin>>b;

		ValType res = 0;



		switch(option){
			case 1:{
				res = manhattanDistance(vals[a], vals[b]);
				cout<<"Res: "<<res<<endl;
				break;
			}
			case 2:{
				res = euclideanDistance(vals[a], vals[b]);
				cout<<"Res: "<<res<<endl;
				break;
			}
			case 3:{
				cout<<"Valor de R?? ->";
				int r = 0;
				cin>>r;
				res = minkowskiDistance(vals[a], vals[b], r);
				cout<<"Res : "<<res<<endl;
				break;
			}
			case 4:{
				res = cosenDistance(vals[a], vals[b]);
				cout<<"Res: "<<res<<endl;
				break;
			}
			case 5:{
				res = pearsonCorrelation(vals[a], vals[b]);
				cout<<"Res: "<<res<<endl;
				break;
			}

		}
	}
}
