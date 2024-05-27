package com.projecte_final.mysong.services;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.projecte_final.mysong.models.ListaReproduccion;
import com.projecte_final.mysong.repository.ListaReproduccionRepository;

import java.util.List;

@Service
public class ListaReproduccionServiceImpl implements ListaReproduccionService {
    
    @Autowired
    private ListaReproduccionRepository listaReproduccionRepository;

    @Override
    public List<ListaReproduccion> findAll() {
        return listaReproduccionRepository.findAll();
    }

    @Override
    public ListaReproduccion findById(Long id) {
        return listaReproduccionRepository.findById(id).orElse(null);
    }

    @Override
    public ListaReproduccion save(ListaReproduccion listaReproduccion) {
        return listaReproduccionRepository.save(listaReproduccion);
    }

    @Override
    public void deleteById(Long id) {
        listaReproduccionRepository.deleteById(id);
    }
    
    @Override
    public List<ListaReproduccion> obtenerListasPorUsuario(String nombreUsuario) {
        return listaReproduccionRepository.findByNombreUsuario(nombreUsuario);
    }
}
