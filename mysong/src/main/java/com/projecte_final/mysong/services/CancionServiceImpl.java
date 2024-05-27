package com.projecte_final.mysong.services;

import org.apache.el.stream.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.projecte_final.mysong.Projection.CancionMetadataProjection;
import com.projecte_final.mysong.models.Cancion;
import com.projecte_final.mysong.modelsDTO.CancionMetadataDTO;
import com.projecte_final.mysong.repository.CancionRepository;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class CancionServiceImpl implements CancionService {

    @Autowired
    private CancionRepository cancionRepository;

    @Override
    public List<Cancion> findAll() {
        return cancionRepository.findAll();
    }

    @Override
    public Cancion findById(Long id) {
        return cancionRepository.findById(id).orElse(null);
    }

    @Override
    public Cancion save(Cancion cancion) {
        return cancionRepository.save(cancion);
    }

    @Override
    public void deleteById(Long id) {
        cancionRepository.deleteById(id);
    }
    @Override
    public List<CancionMetadataDTO> buscarPorNombre(String nombre) {
        List<CancionMetadataProjection> canciones = cancionRepository.findByNombreContaining(nombre);
        List<CancionMetadataDTO> metadataList = new ArrayList<>();
        for (CancionMetadataProjection cancion : canciones) {
            CancionMetadataDTO metadata = new CancionMetadataDTO();
            metadata.setId(cancion.getId());
            metadata.setNombre(cancion.getNombre());
            metadata.setArtista(cancion.getArtista());
            metadata.setAlbum(cancion.getAlbum());
            metadata.setNombreArchivo(cancion.getNombreArchivo());
            // Otros metadatos necesarios
            metadataList.add(metadata);
        }
        return metadataList;
    }



}

