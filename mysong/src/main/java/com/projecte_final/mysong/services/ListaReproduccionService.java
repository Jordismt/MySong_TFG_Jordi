package com.projecte_final.mysong.services;

import java.util.List;

import com.projecte_final.mysong.models.ListaReproduccion;

public interface ListaReproduccionService {
    List<ListaReproduccion> findAll();
    ListaReproduccion findById(Long id);
    ListaReproduccion save(ListaReproduccion listaReproduccion);
    void deleteById(Long id);
	List<ListaReproduccion> obtenerListasPorUsuario(String nombreUsuario);
}

