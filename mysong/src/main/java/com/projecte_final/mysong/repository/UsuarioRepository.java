package com.projecte_final.mysong.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.projecte_final.mysong.models.Usuario;

@Repository
public interface UsuarioRepository extends JpaRepository<Usuario, Long> {
	
	Usuario findByNombre(String nombre);
    // Método personalizado para buscar un usuario por nombre de usuario y contraseña
    Usuario findByNombreAndContraseña(String nombre, String contraseña);
}
