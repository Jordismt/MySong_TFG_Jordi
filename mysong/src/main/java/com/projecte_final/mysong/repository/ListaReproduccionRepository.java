package com.projecte_final.mysong.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.projecte_final.mysong.models.ListaReproduccion;

@Repository
public interface ListaReproduccionRepository extends JpaRepository<ListaReproduccion, Long> {
    // Puedes agregar métodos personalizados aquí si es necesario
	List<ListaReproduccion> findByNombreUsuario(String nombreUsuario);
}

