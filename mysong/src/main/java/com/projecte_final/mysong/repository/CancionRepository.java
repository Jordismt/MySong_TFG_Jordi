package com.projecte_final.mysong.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.projecte_final.mysong.Projection.CancionMetadataProjection;
import com.projecte_final.mysong.models.Cancion;

@Repository
public interface CancionRepository extends JpaRepository<Cancion, Long> {
    // Utiliza una proyección para seleccionar solo los campos necesarios
    List<CancionMetadataProjection> findByNombreContaining(String nombre);
}


