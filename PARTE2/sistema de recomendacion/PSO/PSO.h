#ifndef PSO_H
#define PSO_H

#include <iostream>
#include <stdio.h>
#include <vector>
#include <ctime>
#include <tuple>
#include <algorithm>
#include <iomanip>
#include <fstream>

using namespace std;

typedef double Num;

Num Function(vector<Num> & x){
	Num sum=0;
	for (int i = 0; i < x.size(); ++i)
	 {
	 	sum+=pow(x[i],2);
	 }
	 return sum;
}

Num random(Num max){
	return static_cast <Num> (rand()) / (static_cast <Num> (RAND_MAX/max));
}

Num ValorX(Num lim_inf,Num lim_sup){
	Num aleatorio;
	Num signo;
	for (Num i = lim_inf; i < lim_sup; i+=0.1)
	{

	/*do{
		aleatorio=random(lim_sup);
		//printf("%f\n", aleatorio );
		if(signo>0.5){
			aleatorio=aleatorio*(-1);
		}
	}while(aleatorio<=lim_inf and aleatorio>=lim_sup);
		//printf("%f\n", aleatorio );*/
		aleatorio=random(1);
		if (aleatorio<=0.5)
		{
			return i;
		}
	}
	return lim_inf;
		//return aleatorio;
}


typedef struct {
	vector<Num> x;
	vector<Num> v;
	Num fitness;
}Particula;

void mostrar_particula(Particula p){
	for (int i = 0; i < p.x.size(); ++i)
	{
		printf("x%d = %le;\t",i+1, p.x[i]);
	}
	for (int i = 0; i < p.v.size(); ++i)
	{
		printf("v%d = %le;\t",i+1, p.v[i]);
	}
	//printf("\n");
}

Particula Mejor(vector<Particula> Best){
	Particula X;
	X=Best[0];
	for (int i = 1; i < Best.size(); ++i)
	{
		if (X.fitness>Best[i].fitness)
		{
			X=Best[i];
		}

	}
	return X;
}

class PSO{
public:
	PSO(int iteraciones);
	//~PSO();
	void mostrar_particulas();
	void run();
	Num lim_inf=-5;
	Num lim_sup=5;
	Particula gBest;
	Particula lBest;
	vector<Particula> particulas;
	vector<Particula> pBest;
	int cantidad_de_iteraciones=1000;
	int tam_poblacion=6;
	int dimensiones=2;
};

void PSO::mostrar_particulas(){
	printf("***Cumulo de particulas***\n");
	for (int i = 0; i < tam_poblacion; ++i)
	{
		printf("%d) ", i+1);
		mostrar_particula(particulas[i]);
		printf("\n");
	}
	printf("***Fitness***\n");
	for (int i = 0; i < tam_poblacion; ++i)
	{
		printf("%d) %le \n", i+1,particulas[i].fitness);
	}
}

void PSO::run(){
	//printf("HOLA\n");
	mostrar_particulas();
	Num w,d1,d2,rand1,rand2;
	for (int iteraciones = 0; iteraciones < cantidad_de_iteraciones; ++iteraciones)
	{
		printf("*****Iteracion %d \n", iteraciones+1);
		printf("Mejor: ");
		mostrar_particula(gBest);
		printf("Fitness: %le \n", gBest.fitness );

		w=random(1);
		d1=2.0;
		d2=2.0;
		rand1=random(1);
		rand2=random(1);
		for (int i = 0; i < tam_poblacion; ++i)
		{
			for (int dim = 0; dim < dimensiones; ++dim)
			{
				particulas[i].v[dim]=w*particulas[i].v[dim];
				particulas[i].v[dim]+=d1*rand1*(pBest[i].x[dim]-particulas[i].x[dim]);
				particulas[i].v[dim]+=d2*rand2*(gBest.x[dim]-particulas[i].x[dim]);
				particulas[i].x[dim]=particulas[i].x[dim]+particulas[i].v[dim];
			}
			particulas[i].fitness=Function(particulas[i].x);
			if (pBest[i].fitness>particulas[i].fitness)
			{
				pBest[i]=particulas[i];
			}
		}
		lBest=Mejor(particulas);
		if (lBest.fitness<gBest.fitness)
		{
			gBest=lBest;
		}
		mostrar_particulas();
	}
	printf("Mejor: ");
	mostrar_particula(gBest);
	printf("Fitness: %le \n", gBest.fitness );
}

PSO::PSO(int iteraciones){
	Num x,v;
	//cout<<"HOLa";
	Particula P;
	for (int i = 0; i < tam_poblacion; ++i)
	{
		for (int dim = 0; dim < dimensiones; ++dim)
		{
			x=ValorX(lim_inf,lim_sup);
			v=random(50);//ValorX(lim_inf,lim_sup);
			P.x.push_back(x);
			P.v.push_back(v);
		}
		P.fitness=Function(P.x);
		particulas.push_back(P);
		pBest.push_back(P);
		P.x.clear();
		P.v.clear();
	}
	gBest=Mejor(pBest);
	//mostrar_particula(gBest);
	lBest=Mejor(pBest);
	//mostrar_particula(lBest);
	run();

}


#endif	
