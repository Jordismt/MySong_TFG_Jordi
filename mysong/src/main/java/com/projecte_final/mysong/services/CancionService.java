package com.projecte_final.mysong.services;

import java.util.List;

import com.projecte_final.mysong.models.Cancion;
import com.projecte_final.mysong.modelsDTO.CancionMetadataDTO;

public interface CancionService {
    List<Cancion> findAll();
    Cancion findById(Long id);
    Cancion save(Cancion cancion);
    void deleteById(Long id);
  
    List<CancionMetadataDTO> buscarPorNombre(String nombre);
}

