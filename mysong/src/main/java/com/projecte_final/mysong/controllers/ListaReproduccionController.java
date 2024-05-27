package com.projecte_final.mysong.controllers;

import com.projecte_final.mysong.models.Cancion;
import com.projecte_final.mysong.models.ListaReproduccion;
import com.projecte_final.mysong.models.Usuario;
import com.projecte_final.mysong.services.CancionService;
import com.projecte_final.mysong.services.ListaReproduccionService;
import com.projecte_final.mysong.services.UsuarioService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/listas-reproduccion")
public class ListaReproduccionController {

    @Autowired
    private ListaReproduccionService listaReproduccionService;
    @Autowired
    private UsuarioService usuarioService;
    @Autowired
    private CancionService cancionService;

    @GetMapping
    public ResponseEntity<List<ListaReproduccion>> getAllListasReproduccion() {
        List<ListaReproduccion> listasReproduccion = listaReproduccionService.findAll();
        return new ResponseEntity<>(listasReproduccion, HttpStatus.OK);
    }



    @GetMapping("/listas/{nombreUsuario}")
    public ResponseEntity<List<ListaReproduccion>> obtenerListasPorUsuario(@PathVariable("nombreUsuario") String nombreUsuario) {
        List<ListaReproduccion> listasReproduccion = listaReproduccionService.obtenerListasPorUsuario(nombreUsuario);
        if (listasReproduccion.isEmpty()) {
            return new ResponseEntity<>(HttpStatus.NO_CONTENT);
        }
        return new ResponseEntity<>(listasReproduccion, HttpStatus.OK);
    }

    @PutMapping("/{id}")
    public ResponseEntity<ListaReproduccion> updateListaReproduccion(@PathVariable("id") Long id, @RequestBody ListaReproduccion listaReproduccion) {
        ListaReproduccion existingListaReproduccion = listaReproduccionService.findById(id);
        if (existingListaReproduccion == null) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
        listaReproduccion.setId(id);
        ListaReproduccion updatedListaReproduccion = listaReproduccionService.save(listaReproduccion);
        return new ResponseEntity<>(updatedListaReproduccion, HttpStatus.OK);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteListaReproduccion(@PathVariable("id") Long id) {
        listaReproduccionService.deleteById(id);
        return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }

    // Método para añadir canción a lista de reproducción
    @PostMapping("/{listaId}/canciones/{cancionId}")
    public ResponseEntity<String> addCancionToListaReproduccion(@PathVariable("listaId") Long listaId, @PathVariable("cancionId") Long cancionId) {
        ListaReproduccion listaReproduccion = listaReproduccionService.findById(listaId);
        if (listaReproduccion == null) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }

        Cancion cancion = cancionService.findById(cancionId);
        if (cancion == null) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }

        // Comprobar si la canción ya está en la lista de reproducción
        if (listaReproduccion.getCanciones().contains(cancion)) {
            return new ResponseEntity<String>("La canción ya está en la lista de reproducción", HttpStatus.BAD_REQUEST);
        }

        // Añadir la canción a la lista de reproducción
        listaReproduccion.getCanciones().add(cancion);
        listaReproduccionService.save(listaReproduccion);

        return new ResponseEntity<>(HttpStatus.OK);
    }
    @PostMapping("/{nombreUsuario}")
    public ResponseEntity<ListaReproduccion> createListaReproduccion(@PathVariable("nombreUsuario") String nombreUsuario, @RequestBody ListaReproduccion listaReproduccion) {
        // Buscar al usuario por su nombre
        Usuario usuario = usuarioService.findByNombre(nombreUsuario);
        if (usuario == null) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }

        // Asignar el usuario completo a la lista de reproducción
        listaReproduccion.setUsuario(usuario);
        listaReproduccion.setIdUsuario(usuario.getId());
        listaReproduccion.setNombreUsuario(usuario.getNombre());
        // Guardar la lista de reproducción
        ListaReproduccion newListaReproduccion = listaReproduccionService.save(listaReproduccion);
        return new ResponseEntity<>(newListaReproduccion, HttpStatus.CREATED);
    }

}
