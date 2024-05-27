package com.projecte_final.mysong.services;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.projecte_final.mysong.models.Usuario;
import com.projecte_final.mysong.repository.UsuarioRepository;

import java.util.List;

@Service
public class UsuarioServiceImpl implements UsuarioService {
    
    @Autowired
    private UsuarioRepository usuarioRepository;

    @Override
    public List<Usuario> findAll() {
        return usuarioRepository.findAll();
    }

    @Override
    public Usuario findById(Long id) {
        return usuarioRepository.findById(id).orElse(null);
    }

    @Override
    public Usuario save(Usuario usuario) {
        return usuarioRepository.save(usuario);
    }

    @Override
    public void deleteById(Long id) {
        usuarioRepository.deleteById(id);
    }
    
    // Método para buscar un usuario por nombre de usuario y contraseña
    public Usuario findByUsernameAndPassword(String username, String password) {
        return usuarioRepository.findByNombreAndContraseña(username, password);
    }
    
    public boolean isUsernameAvailable(String username) {
        return usuarioRepository.findByNombre(username) == null;
    }
    @Override
    public Usuario findByNombre(String nombre) {
        return usuarioRepository.findByNombre(nombre);
    }


}

