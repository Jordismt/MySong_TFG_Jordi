package com.projecte_final.mysong.controllers;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.InputStreamResource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.util.Collections;
import java.util.List;

import com.projecte_final.mysong.models.Cancion;
import com.projecte_final.mysong.models.ListaReproduccion;
import com.projecte_final.mysong.models.Usuario;
import com.projecte_final.mysong.modelsDTO.CancionDTO;
import com.projecte_final.mysong.modelsDTO.CancionMetadataDTO;
import com.projecte_final.mysong.services.CancionService;
import com.projecte_final.mysong.services.ListaReproduccionService;
import com.projecte_final.mysong.services.UsuarioService;




@RestController
@RequestMapping("/canciones")
public class CancionController {


	@Autowired
    private CancionService cancionService;
    @Autowired
    private UsuarioService usuarioService;
    @Autowired
    private ListaReproduccionService listaReproduccionService;
    
    @GetMapping
    public ResponseEntity<List<Cancion>> getAllCanciones() {
        List<Cancion> canciones = cancionService.findAll();
        return new ResponseEntity<>(canciones, HttpStatus.OK);
    }
    @GetMapping("/api/canciones")
    public ResponseEntity<List<CancionMetadataDTO>> buscarPorNombre(@RequestParam String nombre) {
        List<CancionMetadataDTO> metadataList = cancionService.buscarPorNombre(nombre);
        return ResponseEntity.ok(metadataList);
    }


    @GetMapping("/{id}")
    public ResponseEntity<Cancion> getCancionById(@PathVariable("id") Long id) {
        Cancion cancion = cancionService.findById(id);
        if (cancion == null) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
        return new ResponseEntity<>(cancion, HttpStatus.OK);
    }

    @PostMapping("/subir-cancion")
    public ResponseEntity<CancionDTO> createCancion(@RequestParam("file") MultipartFile file,
                                                    @RequestParam("nombre") String nombre,
                                                    @RequestParam("artista") String artista,
                                                    @RequestParam("nombreArchivo") String nombreArchivo,
                                                    @RequestParam("likes") int likes,
                                                    @RequestParam("album") String album,
                                                    @RequestParam("usuario") String nombreUsuario,
                                                    @RequestParam("lista_id") Long listaId) {
        try {
            // Buscar al usuario por su nombre
            Usuario usuario = usuarioService.findByNombre(nombreUsuario);
            if (usuario == null) {
                return new ResponseEntity<>(HttpStatus.NOT_FOUND); // Si el usuario no existe, devolvemos un error 404
            }

            // Buscar la lista de reproducción por su ID
            ListaReproduccion listaReproduccion = listaReproduccionService.findById(listaId);
            if (listaReproduccion == null) {
                return new ResponseEntity<>(HttpStatus.NOT_FOUND); // Si la lista no existe, devolvemos un error 404
            }

            // Convertir el archivo a un arreglo de bytes
            byte[] data = file.getBytes();

            // Crear una nueva canción con los datos proporcionados
            Cancion cancion = new Cancion();
            cancion.setNombre(nombre);
            cancion.setArtista(artista);
            cancion.setAlbum(album);
            cancion.setNombreArchivo(nombreArchivo);
            cancion.setLikes(likes);
            cancion.setData(data);
            // Asociar la lista de reproducción a la canción
            cancion.setListasReproduccion(Collections.singletonList(listaReproduccion));
            cancion.setUsuario(usuario);

            // Guardar la canción en la base de datos
            Cancion newCancion = cancionService.save(cancion);

            // Asociar la canción con la lista de reproducción
            listaReproduccion.getCanciones().add(newCancion);
            listaReproduccionService.save(listaReproduccion);

            // Convertir la entidad a DTO
            CancionDTO cancionDTO = new CancionDTO();
            cancionDTO.setId(newCancion.getId());
            cancionDTO.setNombre(newCancion.getNombre());
            cancionDTO.setArtista(newCancion.getArtista());
            cancionDTO.setAlbum(newCancion.getAlbum());
            cancionDTO.setNombreArchivo(newCancion.getNombreArchivo());
            cancionDTO.setLikes(newCancion.getLikes());
            cancionDTO.setUsuarioNombre(usuario.getNombre());

            return new ResponseEntity<>(cancionDTO, HttpStatus.CREATED);
        } catch (IOException e) {
            return new ResponseEntity<>(HttpStatus.INTERNAL_SERVER_ERROR); // Error de servidor
        }
    }




    @PutMapping("/{id}")
    public ResponseEntity<Cancion> updateCancion(@PathVariable("id") Long id, @RequestBody Cancion cancion) {
        Cancion existingCancion = cancionService.findById(id);
        if (existingCancion == null) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
        cancion.setId(id);
        Cancion updatedCancion = cancionService.save(cancion);
        return new ResponseEntity<>(updatedCancion, HttpStatus.OK);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteCancion(@PathVariable("id") Long id) {
        cancionService.deleteById(id);
        return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }

    // Método para dar like a una canción
    @PostMapping("/{id}/like")
    public ResponseEntity<Void> likeCancion(@PathVariable("id") Long id) {
        Cancion cancion = cancionService.findById(id);
        if (cancion == null) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
        // Incrementar el contador de likes de la canción
        cancion.setLikes(cancion.getLikes() + 1);
        cancionService.save(cancion);
        return new ResponseEntity<>(HttpStatus.OK);
    }
    @PostMapping("/usuario/{nombreUsuario}") 
    public ResponseEntity<Cancion> createCancion(@PathVariable("nombreUsuario") String nombreUsuario, @RequestBody Cancion cancion) {
        Usuario usuario = usuarioService.findByNombre(nombreUsuario); // Buscamos al usuario por su nombre
        if (usuario == null) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND); // Si el usuario no existe, devolvemos un error 404
        }
        cancion.setUsuario(usuario); // Asignamos el usuario a la canción
        Cancion newCancion = cancionService.save(cancion);
        return new ResponseEntity<>(newCancion, HttpStatus.CREATED);
    }
    @GetMapping("/stream/{id}")
    public ResponseEntity<InputStreamResource> streamCancion(@PathVariable Long id) {
        Cancion cancion = cancionService.findById(id);
        if (cancion == null || cancion.getData() == null) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }

        ByteArrayInputStream bis = new ByteArrayInputStream(cancion.getData());
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.parseMediaType("audio/mp3"));
        headers.setContentLength(cancion.getData().length);
        headers.setCacheControl("no-cache");
        headers.setPragma("no-cache");
        headers.setExpires(0);

        return new ResponseEntity<>(new InputStreamResource(bis), headers, HttpStatus.OK);
    }
}


