#ifndef FILEOP_H
#define FILEOP_H

#include <iostream>
#include <fstream>
#include <string>
#include "Utils.h"

vector<ValVec> getBdVals(string file, int n){
	ifstream valsFile(file.c_str());
	vector<ValVec> vals(n);
	string word = "";
	int count = 0;
	while(valsFile>>word){
		if(word == "-") vals[count].push_back(NULL_VAL);
		else vals[count].push_back(stoVT(word));
		count++;
		if(count == n) count = 0;
	}
	valsFile.close();
	return vals;
}

vector<string> getBdNames(string file){
	vector<string> names;
	ifstream namesFile(file.c_str());
	string word = "";
	while(namesFile>>word){
		names.push_back(word);
	}
	namesFile.close();
	return names;
}


vector<Registro> getBd(string fileName, char delimit){
	vector<Registro> res;
	ifstream bdFile(fileName.c_str());
	string word = "";
	char line[512];
	while(bdFile.getline(line,512)){
		word = string(line);
		res.push_back(splitString(word, delimit));
	}
	bdFile.close();
	return res;
}

vector<Registro> getBd(string fileName, char delimit, int left_limit, int rigth_limit){
	vector<Registro> res;
	ifstream bdFile(fileName.c_str());
	string word = "";
	char line[512];
	int count = 0;
	while(bdFile.getline(line,512)){
		count++;
		if(count - 1 < left_limit) continue;
		if(count == rigth_limit) break;
		word = string(line);
		res.push_back(splitString(word, delimit));
	}
	bdFile.close();
	return res;
}

#endif
