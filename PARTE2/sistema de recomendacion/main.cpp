#include <iostream>
#include <fstream>
#include <cmath>
#include <map>
#include <thread>
#include "Distancias.h"
#include "FileOp.h"
#include "Algoritmos.h"
#include "MyTime.h"

using namespace std;

#define NUM_THREADS 4
#define MAX_RATING 5

typedef int MovieId;
typedef string MovieName;
typedef string MovieCategories;
typedef tuple<MovieName, MovieCategories> MovieRegister;

typedef int UserId;
typedef ValType Valoration;
typedef tuple<MovieId, Valoration> InterRegister;

typedef map<MovieId, Valoration> InterRegisterMap;

MyTime mytime;


void printInters(InterRegisterMap interMap){
	for(auto iter = interMap.begin(); iter != interMap.end(); ++iter){
		cout<<iter->first<<" "<<iter->second<<endl;
	}
}

void printMovie(MovieRegister movie){
	cout<<get<0>(movie)<<" "<<get<1>(movie)<<endl;
}

void getSlope(vector<InterRegisterMap> * valsByUser, map<MovieId,map<UserId,ValType>> * valsByProduct,
				map<MovieId, MovieRegister>::iterator ini, map<MovieId, MovieRegister>::iterator end,
				UserId userId, vector<tuple<MovieId,Valoration>> * valoraciones){
	InterRegisterMap::iterator findRes;
	map<MovieId,map<UserId,ValType>>::iterator findMovieRes;
	MovieLensVectorDesviacion desVec;
	ValType res = 0;
	for(auto iter = ini; iter != end; ++iter){
		findMovieRes = valsByProduct->find(iter->first);
		if(findMovieRes == valsByProduct->end()) continue;
		findRes = (*valsByUser)[userId].find(iter->first);
		if(findRes != (*valsByUser)[userId].end()) continue;

		desVec = getvectorDesviacion(*valsByProduct, *valsByUser, userId, iter->first);
		res = slopeOne(desVec, *valsByProduct, *valsByUser, userId, iter->first);
		valoraciones->push_back(make_tuple(iter->first,res));
	}
}

int main(){
	cout<<"Cargando Base de Datos..."<<endl;
	mytime.init();

	auto bdMovies = getBd("ml/movies.csv", ';');
	auto bdInter = getBd("ml/ratings.csv", ',');

	mytime.end();
	cout<<"Done->";
	mytime.print();

	UserId id = 0;

	cout<<"Generando estructura Movies..."<<endl;
	mytime.init();
	map<MovieId, MovieRegister> movieVec;
	for(auto iter = bdMovies.begin(); iter != bdMovies.end(); ++iter){
		id = stoi((*iter)[0]);
		movieVec[id] = make_tuple((*iter)[1], (*iter)[2]);
	}
	mytime.end();
	cout<<"Done->";
	mytime.print();


	cout<<"Generando estructura InterbyUser..."<<endl;
	mytime.init();

	int numUsers = 671;

	vector<InterRegisterMap> valsByUser(numUsers);
	Valoration val = 0;

	MovieId id2 = 0;

	for(auto iter = bdInter.begin(); iter != bdInter.end(); ++iter){
		id = stoi((*iter)[0]) - 1;
		id2 = stoi((*iter)[1]);
		val = stof((*iter)[2]);
		valsByUser[id][id2] = val;
	}
	mytime.end();
	cout<<"Done->";
	mytime.print();

	cout<<"Generando estructura InterbyProduct..."<<endl;
	mytime.init();

	map<MovieId,map<UserId,ValType>> valsByProduct;
	for(auto iter = bdInter.begin(); iter != bdInter.end(); ++iter){
		id = stoi((*iter)[0]) - 1;
		id2 = stoi((*iter)[1]);
		val = stof((*iter)[2]);
		valsByProduct[id2][id] = val;
	}
	mytime.end();
	cout<<"Done->";
	mytime.print();

	bdInter.clear();
	bdMovies.clear();

	UserId userId = 0;
	MovieId movieId = 0;
	int option = 0;
	int bd = 0;


	while(true){
		cout<<endl<<"1) Busqueda"<<endl;
		cout<<"2) Prediccion"<<endl;
		cout<<"3) Nuevo Usuario"<<endl;
		cout<<"4) Iniciar Sesion"<<endl;
		cout<<"5) Recomendacion1"<<endl;
		cout<<"6) Recomendacion2"<<endl;
		cout<<"Opcion->";
		cin>>option;
		cout<<endl;
		switch(option){
			case 1:{
				cout<<"1) Movie"<<endl;
				cout<<"2) Inter"<<endl;
				cout<<"Opcion->";
				cin>>bd;
				cout<<endl;
				switch(bd){
					case 1:{
						cout<<"Id->";
						cin>>movieId;
						printMovie(movieVec[movieId]);
						break;
					}
					case 2:{
						cout<<"Id->";
						cin>>userId;
						userId--;
						printInters(valsByUser[userId]);
						break;
					}
				}
				break;
			}
			case 2:{
				//ATENCIOOOOONNNN!!!!! el id del usuario tiene que resarce uno.
				cout<<"UserId->";
				cin>>userId;
				userId--;
				cout<<"MovieId->";
				cin>>movieId;
				auto findRes = valsByUser[userId].find(movieId);
				if(findRes != valsByUser[userId].end()){
					cout<<"El libro ya ha sido ranqueado por este usuario"<<endl;
					break;
				}
				cout<<"Generando vector de desviacion..."<<endl;
				mytime.init();
				auto desVec = getvectorDesviacion(valsByProduct, valsByUser, userId, movieId);
				mytime.end();
				cout<<"Done->";
				mytime.print();

				cout<<"Calculando SlopeOne..."<<endl;
				mytime.init();
				ValType res = slopeOne(desVec, valsByProduct, valsByUser, userId, movieId);
				mytime.end();
				cout<<"Done->";
				mytime.print();

				cout<<"El usuario "<<userId + 1<<" pondría el puntaje "<<res<<" al libro "<<get<0>(movieVec[movieId])<<endl;
				break;
			}
			case 3:{
				numUsers++;
				valsByUser.push_back(InterRegisterMap());
				cout<<"Nuevo usuario creado"<<endl;
				cout<<"Id del nuevo usuario->"<<numUsers<<endl;
				break;
			}
			case 4:{
				cout<<"UserId->";
				cin>>userId;
				userId--;
				cout<<"Bienvenido usuario "<<userId + 1<<endl;
				bool flag = true;
				Valoration val = 0;
				while(flag){
					cout<<"1) Mis ranqueados"<<endl;
					cout<<"2) Ranquear pelicula"<<endl;
					cout<<"3) Cerrar Sesion"<<endl;
					cout<<"Opcion->";
					cin>>option;
					cout<<endl;
					switch(option){
						case 1:{
							printInters(valsByUser[userId]);
							break;
						}
						case 2:{
							cout<<"MovieId->";
							cin>>movieId;
							auto findRes = valsByUser[userId].find(movieId);
							if(findRes != valsByUser[userId].end()){
								cout<<"La pelicula ya ha sido ranqueada por este usuario"<<endl;
								cout<<"Quiere cambiar el puntaje?? 1) Si 2) No"<<endl;
								cout<<"Opcion->";
								cin>>option;
								if(option == 2) break;
							}
							cout<<"Puntaje->";
							cin>>val;
							valsByUser[userId][movieId] = val;
							valsByProduct[movieId][userId] = val;
							cout<<"Pelicula ranqueada correctamente"<<endl<<endl;
							break;
						}
						case 3:{
							flag = false;
							break;
						}
					}
				}
				break;
			}
			case 5:{
				int k;
				//cout<<"UserId->";
				//cin>>userId;
				//userId--;
				cout<<"K->";
				cin>>k;
				for (size_t i = 0; i < 15; i++) {
					userId=i;
					vector<tuple<MovieId,Valoration>> valoraciones;
					InterRegisterMap::iterator findRes;
					map<MovieId,map<UserId,ValType>>::iterator findMovieRes;
					MovieLensVectorDesviacion desVec;
					ValType res = 0;
					int count = 0;
					//cout<<"Generando recomendaciones...";
					mytime.init();
					for(auto iter = movieVec.begin(); iter != movieVec.end(); ++iter){
					//	cout<<count++<<"/"<<movieVec.size()<<endl;
						findMovieRes = valsByProduct.find(iter->first);
						if(findMovieRes == valsByProduct.end()) continue;
						findRes = valsByUser[userId].find(iter->first);
						if(findRes != valsByUser[userId].end()) continue;

						desVec = getvectorDesviacion(valsByProduct, valsByUser, userId, iter->first);
						res = slopeOne(desVec, valsByProduct, valsByUser, userId, iter->first);
						if(res > 5) continue;
						valoraciones.push_back(make_tuple(iter->first,res));
					}
					sort(valoraciones.begin(), valoraciones.end(), [](tuple<MovieId,Valoration> a, tuple<MovieId, Valoration> b){
						return get<1>(a) > get<1>(b);
					});
					if(valoraciones.size() > k) valoraciones.erase(valoraciones.begin() + k, valoraciones.end());
					for(auto resTuple : valoraciones){
						//cout<<get<1>(resTuple)<<" -> "<<get<0>(movieVec[get<0>(resTuple)])<<endl;
					}
					mytime.end();
					//cout<<"Done->";
					mytime.print();

				}
				break;
			}
			case 6:{
				int k;
				//cout<<"UserId->";
				//cin>>userId;
				//userId--;
				cout<<"K->";
				cin>>k;
				for (size_t i = 0; i < 15; i++) {

					userId=i;
					vector<tuple<MovieId,Valoration>> valoraciones;
					vector<tuple<MovieId,Valoration>> valoracionesRes;
					InterRegisterMap::iterator findRes;
					map<MovieId,map<UserId,ValType>>::iterator findMovieRes;
					MovieLensVectorDesviacion desVec;
					ValType res = 0;
					int count = 0;
					//cout<<"Generando recomendaciones..."<<endl;
					mytime.init();
					for(auto iter = movieVec.begin(); iter != movieVec.end(); ++iter){
						if(valoracionesRes.size() == k) break;
						//cout<<count++<<"/"<<movieVec.size()<<endl;
						findMovieRes = valsByProduct.find(iter->first);
						if(findMovieRes == valsByProduct.end()) continue;
						findRes = valsByUser[userId].find(iter->first);
						if(findRes != valsByUser[userId].end()) continue;

						desVec = getvectorDesviacion(valsByProduct, valsByUser, userId, iter->first);
						res = slopeOne(desVec, valsByProduct, valsByUser, userId, iter->first);
						valoraciones.push_back(make_tuple(iter->first,res));
						//cout<<res<<endl;
						if(res >= (ValType) MAX_RATING - 0.00005){
							valoracionesRes.push_back(make_tuple(iter->first,res));
						}

					}
					if(valoraciones.size() == k){
						for(auto resTuple : valoracionesRes){
							//cout<<get<1>(resTuple)<<" -> "<<get<0>(movieVec[get<0>(resTuple)])<<endl;
						}
					}
					else{
						sort(valoraciones.begin(), valoraciones.end(), [](tuple<MovieId,Valoration> a, tuple<MovieId, Valoration> b){
							return get<1>(a) > get<1>(b);
						});
						if(valoraciones.size() > k) valoraciones.erase(valoraciones.begin() + k, valoraciones.end());
						for(auto resTuple : valoraciones){
							//cout<<get<1>(resTuple)<<" -> "<<get<0>(movieVec[get<0>(resTuple)])<<endl;
						}
					}
					mytime.end();
					//cout<<"Done->";
					mytime.print();
				}


				break;
			}
			/*case 7:{
				int k;
				cout<<"UserId->";
				cin>>userId;
				userId--;
				cout<<"K->";
				cin>>k;
				vector<tuple<MovieId,Valoration>> valoraciones;
				InterRegisterMap::iterator findRes;
				map<MovieId,map<UserId,ValType>>::iterator findMovieRes;
				MovieLensVectorDesviacion desVec;
				ValType res = 0;

				thread threads[NUM_THREADS];
				vector<tuple<MovieId,Valoration>> * tRes[NUM_THREADS];
				int h = movieVec.size() / NUM_THREADS;
				map<MovieId, MovieRegister>::iterator ini = movieVec.begin();
				map<MovieId, MovieRegister>::iterator end = ini;
				for(int i = 0; i < NUM_THREADS; i++){
					tRes[i] = new vector<tuple<MovieId,Valoration>>();
					if(i == NUM_THREADS - 1) end = movieVec.end();
					else{
						for(int j = 0; j < h; j++){
							++end;
						}
					}
					threads[i] = thread(getSlope,&valsByUser,&valsByProduct,ini,end,userId,tRes[i]);
					ini = end;
				}

				for(int i = 0; i < NUM_THREADS; i++){
					threads[i].join();
					valoraciones.insert(valoraciones.end(), tRes[i]->begin(), tRes[i]->end());
				}
				sort(valoraciones.begin(), valoraciones.end(), [](tuple<MovieId,Valoration> a, tuple<MovieId, Valoration> b){
					return get<1>(a) > get<1>(b);
				});
				if(valoraciones.size() > k) valoraciones.erase(valoraciones.begin() + k, valoraciones.end());
				for(auto resTuple : valoraciones){
					cout<<get<1>(resTuple)<<" -> "<<get<0>(movieVec[get<0>(resTuple)])<<endl;
				}
				break;
			}*/
		}
	}
}
