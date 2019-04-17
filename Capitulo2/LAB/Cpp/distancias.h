#ifndef DISTANCIAS_H
#define DISTANCIAS_H

#include <iostream>
#include <functional>
#include "Utils.h"

typedef function<ValType(ValVec &, ValVec &)> DistanceFunction;

ValType manhattanDistance(ValVec & x, ValVec & y){
	if(x.size() != y.size()) return 0;
	ValType res = 0;
	for(int i = 0; i < x.size(); i++){
		if(x[i] == NULL_VAL or y[i] == NULL_VAL) continue;
		else res += abs(x[i] - y[i]);
	}
	return res;
}

ValType euclideanDistance(ValVec & x, ValVec & y){
	if(x.size() != y.size()) return 0;
	ValType res = 0;
	for(int i = 0; i < x.size(); i++){
		if(x[i] == NULL_VAL or y[i] == NULL_VAL) continue;
		else res += pow(x[i] - y[i], 2);
	}
	return (ValType) sqrt(res);
}

ValType minkowskiDistance(ValVec & x, ValVec & y, int r){
	if(x.size() != y.size()) return 0;
	ValType res = 0;
	for(int i = 0; i < x.size(); i++){
		if(x[i] == NULL_VAL or y[i] == NULL_VAL) continue;
		res += pow(abs(x[i] - y[i]), r);
	}
	if(r == 2) return (ValType) sqrt(res);
	return res;
}

ValType pearsonCorrelation(ValVec & x, ValVec & y){
  ValType res = 0;
	ValVec xx;
	ValVec yy;
	tie(xx,yy) = deleteNulls(x,y);
	ValType n = xx.size();
	//cout<<"N->"<<n<<endl;
  ValType div=(sqrt(sumatoriaCuadratica(xx) - pow(sumatoria(xx),2) / n) * sqrt(sumatoriaCuadratica(yy) - pow(sumatoria(yy),2) / n));
  return (ValType) ((dotProduct(xx,yy) - (sumatoria(xx) * sumatoria(yy) / n)) / div);
}

ValType cosenDistance(ValVec & x, ValVec & y){
	if(x.size() != y.size()) return 0;
	if((vectorModule(x) * vectorModule(y)) == 0) return -1;
	return dotProduct(x,y) / (vectorModule(x) * vectorModule(y));
}


#endif
