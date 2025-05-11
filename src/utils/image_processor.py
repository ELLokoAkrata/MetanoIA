"""
Módulo para procesar y gestionar imágenes en MetanoIA.
"""
import os
import base64
import uuid
from PIL import Image
import io
import logging

from src.utils.logger import setup_logger

logger = setup_logger("ImageProcessor")

class ImageProcessor:
    """Clase para procesar y gestionar imágenes."""
    
    @staticmethod
    def resize_image(image_data, max_pixels=33177600, output_format="JPEG"):
        """
        Redimensiona una imagen si excede el número máximo de píxeles.
        
        Args:
            image_data (bytes): Datos binarios de la imagen.
            max_pixels (int): Número máximo de píxeles permitidos.
            output_format (str): Formato de salida de la imagen.
            
        Returns:
            bytes: Datos binarios de la imagen redimensionada.
        """
        try:
            # Abrir la imagen desde los datos binarios
            image = Image.open(io.BytesIO(image_data))
            
            # Calcular el número actual de píxeles
            width, height = image.size
            current_pixels = width * height
            
            # Si la imagen no excede el límite, devolverla sin cambios
            if current_pixels <= max_pixels:
                logger.info(f"La imagen no necesita redimensionamiento: {width}x{height} = {current_pixels} píxeles")
                return image_data
            
            # Calcular la relación de redimensionamiento
            ratio = (max_pixels / current_pixels) ** 0.5
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            
            logger.info(f"Redimensionando imagen de {width}x{height} ({current_pixels} píxeles) a {new_width}x{new_height} ({new_width * new_height} píxeles)")
            
            # Redimensionar la imagen manteniendo la relación de aspecto
            resized_image = image.resize((new_width, new_height), Image.LANCZOS)
            
            # Convertir la imagen redimensionada a bytes
            output_buffer = io.BytesIO()
            resized_image.save(output_buffer, format=output_format)
            
            return output_buffer.getvalue()
            
        except Exception as e:
            logger.error(f"Error al redimensionar la imagen: {str(e)}")
            logger.exception("Detalles del error:")
            return image_data  # Devolver la imagen original en caso de error
    
    @staticmethod
    def encode_image(image_data):
        """
        Codifica los datos de una imagen en base64.
        
        Args:
            image_data (bytes): Datos binarios de la imagen.
            
        Returns:
            str: Imagen codificada en base64.
        """
        try:
            return base64.b64encode(image_data).decode('utf-8')
        except Exception as e:
            logger.error(f"Error al codificar la imagen en base64: {str(e)}")
            logger.exception("Detalles del error:")
            return ""
    
    @staticmethod
    def save_uploaded_image(uploaded_file, directory="temp_images"):
        """
        Guarda una imagen subida por el usuario.
        
        Args:
            uploaded_file: Archivo subido por el usuario.
            directory (str): Directorio donde guardar la imagen.
            
        Returns:
            tuple: (str, bytes) - Ruta al archivo guardado y datos binarios.
        """
        try:
            # Crear el directorio si no existe
            os.makedirs(directory, exist_ok=True)
            
            # Generar un nombre único para el archivo
            file_extension = os.path.splitext(uploaded_file.name)[1].lower()
            filename = f"{uuid.uuid4()}{file_extension}"
            filepath = os.path.join(directory, filename)
            
            # Leer los datos del archivo
            image_data = uploaded_file.getvalue()
            
            # Redimensionar la imagen si es necesario
            processed_image_data = ImageProcessor.resize_image(image_data)
            
            # Guardar la imagen procesada
            with open(filepath, "wb") as f:
                f.write(processed_image_data)
            
            logger.info(f"Imagen guardada en {filepath}")
            
            return filepath, processed_image_data
            
        except Exception as e:
            logger.error(f"Error al guardar la imagen: {str(e)}")
            logger.exception("Detalles del error:")
            return None, None
    
    @staticmethod
    def validate_image(image_data, max_size_mb=20):
        """
        Valida que una imagen cumpla con los requisitos.
        
        Args:
            image_data (bytes): Datos binarios de la imagen.
            max_size_mb (int): Tamaño máximo en MB.
            
        Returns:
            tuple: (bool, str) - Validez y mensaje de error si aplica.
        """
        try:
            # Verificar el tamaño
            size_mb = len(image_data) / (1024 * 1024)
            if size_mb > max_size_mb:
                return False, f"La imagen es demasiado grande: {size_mb:.2f}MB (máximo {max_size_mb}MB)"
            
            # Verificar que sea una imagen válida
            try:
                Image.open(io.BytesIO(image_data))
            except:
                return False, "El archivo no es una imagen válida"
            
            return True, ""
            
        except Exception as e:
            logger.error(f"Error al validar la imagen: {str(e)}")
            logger.exception("Detalles del error:")
            return False, f"Error al validar la imagen: {str(e)}"


# Funciones auxiliares para facilitar el uso desde la interfaz
def resize_image(image_path, max_pixels=33177600, max_size_mb=4):
    """
    Redimensiona una imagen si excede el número máximo de píxeles o tamaño.
    
    Args:
        image_path (str): Ruta al archivo de imagen.
        max_pixels (int): Número máximo de píxeles permitidos (33177600 para Groq).
        max_size_mb (int): Tamaño máximo en MB (4MB para imágenes base64 en Groq).
        
    Returns:
        str: Ruta a la imagen redimensionada.
    """
    try:
        # Leer la imagen desde el archivo
        with open(image_path, "rb") as f:
            image_data = f.read()
        
        # Verificar el tamaño original
        original_size_mb = len(image_data) / (1024 * 1024)
        logger.info(f"Tamaño original de la imagen: {original_size_mb:.2f}MB")
        
        # Abrir la imagen para obtener dimensiones
        image = Image.open(io.BytesIO(image_data))
        width, height = image.size
        current_pixels = width * height
        logger.info(f"Dimensiones originales: {width}x{height} = {current_pixels} píxeles")
        
        # Determinar si necesitamos redimensionar por píxeles o tamaño
        needs_resize_pixels = current_pixels > max_pixels
        needs_resize_size = original_size_mb > max_size_mb
        
        if not (needs_resize_pixels or needs_resize_size):
            logger.info("La imagen ya cumple con los límites de tamaño y resolución")
            return image_path
        
        # Redimensionar la imagen
        if needs_resize_pixels:
            # Calcular la relación de redimensionamiento por píxeles
            ratio_pixels = (max_pixels / current_pixels) ** 0.5
            new_width_pixels = int(width * ratio_pixels)
            new_height_pixels = int(height * ratio_pixels)
            logger.info(f"Redimensionando por píxeles a {new_width_pixels}x{new_height_pixels}")
            resized_image = image.resize((new_width_pixels, new_height_pixels), Image.LANCZOS)
        else:
            resized_image = image
        
        # Comprimir la imagen si aún excede el tamaño máximo
        quality = 95  # Calidad inicial
        output_buffer = io.BytesIO()
        resized_image.save(output_buffer, format="JPEG", quality=quality)
        compressed_data = output_buffer.getvalue()
        compressed_size_mb = len(compressed_data) / (1024 * 1024)
        
        # Reducir la calidad progresivamente hasta que la imagen sea lo suficientemente pequeña
        while compressed_size_mb > max_size_mb and quality > 30:
            quality -= 5
            output_buffer = io.BytesIO()
            resized_image.save(output_buffer, format="JPEG", quality=quality)
            compressed_data = output_buffer.getvalue()
            compressed_size_mb = len(compressed_data) / (1024 * 1024)
            logger.info(f"Comprimiendo imagen con calidad {quality}, tamaño: {compressed_size_mb:.2f}MB")
        
        # Guardar la imagen redimensionada/comprimida
        resized_path = f"{os.path.splitext(image_path)[0]}_optimized.jpg"  # Siempre usar .jpg para mejor compresión
        with open(resized_path, "wb") as f:
            f.write(compressed_data)
        
        # Verificar dimensiones finales
        final_image = Image.open(io.BytesIO(compressed_data))
        final_width, final_height = final_image.size
        final_pixels = final_width * final_height
        
        logger.info(f"Imagen optimizada guardada en {resized_path}")
        logger.info(f"Dimensiones finales: {final_width}x{final_height} = {final_pixels} píxeles")
        logger.info(f"Tamaño final: {compressed_size_mb:.2f}MB")
        
        return resized_path
        
    except Exception as e:
        logger.error(f"Error al redimensionar la imagen: {str(e)}")
        logger.exception("Detalles del error:")
        return image_path  # Devolver la ruta original en caso de error

def encode_image_to_base64(image_path):
    """
    Codifica una imagen en base64.
    
    Args:
        image_path (str): Ruta al archivo de imagen.
        
    Returns:
        str: Imagen codificada en base64.
    """
    try:
        # Leer la imagen desde el archivo
        with open(image_path, "rb") as f:
            image_data = f.read()
        
        # Verificar el tamaño de la imagen
        size_mb = len(image_data) / (1024 * 1024)
        logger.info(f"Tamaño de la imagen a codificar: {size_mb:.2f}MB")
        
        if size_mb > 4:
            logger.warning(f"La imagen es demasiado grande ({size_mb:.2f}MB) para codificar en base64. Groq limita a 4MB.")
            logger.warning("Considera redimensionar la imagen primero con resize_image()")
        
        # Codificar usando la clase ImageProcessor
        base64_string = ImageProcessor.encode_image(image_data)
        
        # Verificar el tamaño del string base64
        base64_size_mb = len(base64_string) * 3 / 4 / 1024 / 1024  # Estimación aproximada
        logger.info(f"Tamaño aproximado de la imagen codificada en base64: {base64_size_mb:.2f}MB")
        
        return base64_string
        
    except Exception as e:
        logger.error(f"Error al codificar la imagen: {str(e)}")
        logger.exception("Detalles del error:")
        return ""

def save_uploaded_image(uploaded_file, image_id=None, directory="temp_images"):
    """
    Guarda una imagen subida por el usuario.
    
    Args:
        uploaded_file: Archivo subido por el usuario.
        image_id (str): ID único para la imagen (opcional).
        directory (str): Directorio donde guardar la imagen.
        
    Returns:
        str: Ruta al archivo guardado.
    """
    try:
        # Crear el directorio si no existe
        os.makedirs(directory, exist_ok=True)
        
        # Generar un nombre para el archivo basado en el ID o generar uno nuevo
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        if not image_id:
            image_id = str(uuid.uuid4())
        filename = f"{image_id}{file_extension}"
        filepath = os.path.join(directory, filename)
        
        # Leer los datos del archivo
        image_data = uploaded_file.getvalue()
        
        # Guardar la imagen original (sin procesar)
        with open(filepath, "wb") as f:
            f.write(image_data)
        
        logger.info(f"Imagen guardada en {filepath}")
        
        return filepath
        
    except Exception as e:
        logger.error(f"Error al guardar la imagen: {str(e)}")
        logger.exception("Detalles del error:")
        return None

def validate_uploaded_image(uploaded_file, max_size_mb=20):
    """
    Valida que una imagen subida cumpla con los requisitos.
    
    Args:
        uploaded_file: Archivo subido por el usuario.
        max_size_mb (int): Tamaño máximo en MB.
        
    Returns:
        tuple: (bool, str) - Validez y mensaje de error si aplica.
    """
    try:
        # Verificar que el archivo existe
        if uploaded_file is None:
            return False, "No se ha subido ningún archivo"
        
        # Leer los datos del archivo
        image_data = uploaded_file.getvalue()
        
        # Validar usando la clase ImageProcessor
        return ImageProcessor.validate_image(image_data, max_size_mb)
        
    except Exception as e:
        logger.error(f"Error al validar la imagen subida: {str(e)}")
        logger.exception("Detalles del error:")
        return False, f"Error al validar la imagen: {str(e)}"
