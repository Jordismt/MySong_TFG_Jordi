package com.projecte_final.mysong.controllers;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import com.projecte_final.mysong.models.Usuario;
import com.projecte_final.mysong.services.UsuarioService;

import java.util.List;

@RestController
@RequestMapping("/usuarios")
public class UsuarioController {

    @Autowired
    private UsuarioService usuarioService;
    
    
    @GetMapping("/check-username")
    public ResponseEntity<Boolean> checkUsernameAvailability(@RequestParam String username) {
        boolean available = usuarioService.isUsernameAvailable(username);
        return ResponseEntity.ok(available);
    }
    // Endpoint para iniciar sesión
    @PostMapping("/login")
    public ResponseEntity<String> login(@RequestParam String username, @RequestParam String password) {
        Usuario usuario = usuarioService.findByUsernameAndPassword(username, password);
        if (usuario != null) {
            return ResponseEntity.ok("Inicio de sesión exitoso");
        } else {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("Usuario o contraseña incorrectos");
        }
    }
    @GetMapping
    public ResponseEntity<List<Usuario>> getAllUsuarios() {
        List<Usuario> usuarios = usuarioService.findAll();
        return new ResponseEntity<>(usuarios, HttpStatus.OK);
    }
    
    @GetMapping("/by-username/{username}")
    public ResponseEntity<Usuario> getUsuarioByUsername(@PathVariable String username) {
        Usuario usuario = usuarioService.findByNombre(username);
        if (usuario != null) {
            return ResponseEntity.ok(usuario);
        } else {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(null);
        }
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<Usuario> getUsuarioById(@PathVariable("id") Long id) {
        Usuario usuario = usuarioService.findById(id);
        if (usuario == null) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
        return new ResponseEntity<>(usuario, HttpStatus.OK);
    }

    @PostMapping
    public ResponseEntity<Usuario> createUsuario(@RequestBody Usuario usuario) {
        Usuario newUsuario = usuarioService.save(usuario);
        return new ResponseEntity<>(newUsuario, HttpStatus.CREATED);
    }
    @PutMapping("/nombre/{nombre}")
    public ResponseEntity<Usuario> updateUsuario(@PathVariable("nombre") String nombre, @RequestBody Usuario usuario) {
        Usuario existingUsuario = usuarioService.findByNombre(nombre);
        if (existingUsuario == null) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
        existingUsuario.setNombre(usuario.getNombre()); // Actualiza el nombre del usuario
        Usuario updatedUsuario = usuarioService.save(existingUsuario); // Guarda los cambios en la base de datos
        return new ResponseEntity<>(updatedUsuario, HttpStatus.OK);
    }
    @PutMapping("/{id}")
    public ResponseEntity<Usuario> updateUsuario(@PathVariable("id") Long id, @RequestBody Usuario usuario) {
        Usuario existingUsuario = usuarioService.findById(id);
        if (existingUsuario == null) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
        usuario.setId(id);
        Usuario updatedUsuario = usuarioService.save(usuario);
        return new ResponseEntity<>(updatedUsuario, HttpStatus.OK);
    }


    @DeleteMapping("/{nombre}")
    public ResponseEntity<Void> deleteUsuario(@PathVariable("nombre") String nombreUsuario) {
        Usuario usuario = usuarioService.findByNombre(nombreUsuario);
        if (usuario == null) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
        usuarioService.deleteById(usuario.getId());
        return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }
}
