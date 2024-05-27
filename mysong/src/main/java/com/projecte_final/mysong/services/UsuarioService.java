package com.projecte_final.mysong.services;
import java.util.List;

import com.projecte_final.mysong.models.Usuario;
public interface UsuarioService {
    List<Usuario> findAll();
    Usuario findById(Long id);
    Usuario save(Usuario usuario);
    void deleteById(Long id);
    boolean isUsernameAvailable(String username);
    Usuario findByNombre(String nombre);
    // Método para buscar un usuario por nombre de usuario y contraseña
	Usuario findByUsernameAndPassword(String username, String password);
}
