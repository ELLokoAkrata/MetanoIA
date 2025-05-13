"""
Módulo para procesar y gestionar imágenes en MetanoIA.
"""
import os
import base64
import uuid
import time
import datetime
from PIL import Image
import io
import logging
import glob
from typing import List, Tuple

from src.utils.logger import setup_logger

logger = setup_logger("ImageProcessor")

class ImageProcessor:
    """Clase para procesar y gestionar imágenes."""
    
    @staticmethod
    def resize_image(image_data, max_pixels=33177600, max_size_mb=4, preserve_content=True):
        """
        Redimensiona una imagen si excede el número máximo de píxeles o tamaño.
        Preserva la relación de aspecto y el contenido importante de la imagen.
        
        Args:
            image_data (bytes): Datos binarios de la imagen.
            max_pixels (int): Número máximo de píxeles permitidos.
            max_size_mb (int): Tamaño máximo en MB.
            preserve_content (bool): Si es True, intenta preservar el contenido importante al redimensionar.
            
        Returns:
            bytes: Datos binarios de la imagen redimensionada.
        """
        try:
            # Abrir la imagen desde los datos binarios
            image = Image.open(io.BytesIO(image_data))
            
            # Calcular el número actual de píxeles y tamaño
            width, height = image.size
            current_pixels = width * height
            original_size_mb = len(image_data) / (1024 * 1024)
            
            # Determinar si necesitamos redimensionar por píxeles o tamaño
            needs_resize_pixels = current_pixels > max_pixels
            needs_resize_size = original_size_mb > max_size_mb
            
            # Si la imagen no excede los límites, devolverla sin cambios
            if not (needs_resize_pixels or needs_resize_size):
                logger.info(f"La imagen no necesita redimensionamiento: {width}x{height} = {current_pixels} píxeles, {original_size_mb:.2f}MB")
                return image_data
            
            # Calcular dimensiones óptimas basadas en restricciones
            if needs_resize_pixels:
                # Calcular la relación de redimensionamiento por píxeles
                ratio_pixels = (max_pixels / current_pixels) ** 0.5
                new_width = int(width * ratio_pixels)
                new_height = int(height * ratio_pixels)
                logger.info(f"Redimensionamiento necesario por píxeles: {new_width}x{new_height}")
            else:
                new_width = width
                new_height = height
            
            # Si la imagen es muy grande en tamaño pero no en píxeles, estimar dimensiones
            if needs_resize_size and not needs_resize_pixels:
                # Estimar factor de reducción basado en tamaño
                size_ratio = max_size_mb / original_size_mb
                # Aplicar un factor de seguridad (0.8) para compensar la compresión
                pixel_ratio = (size_ratio * 0.8) ** 0.5
                new_width = int(width * pixel_ratio)
                new_height = int(height * pixel_ratio)
                logger.info(f"Redimensionamiento estimado por tamaño: {new_width}x{new_height}")
            
            # Redimensionar la imagen preservando contenido si es necesario
            if preserve_content and (width > 1000 or height > 1000):
                logger.info("Usando redimensionamiento inteligente para preservar contenido importante")
                # Usar un algoritmo de mejor calidad para imágenes grandes
                resizing_algorithm = Image.LANCZOS
                
                # Si la imagen es muy grande, usar un enfoque en dos pasos para mejor calidad
                if width > 3000 or height > 3000:
                    # Primer paso: reducir a un tamaño intermedio
                    intermediate_width = min(width, int(new_width * 1.5))
                    intermediate_height = min(height, int(new_height * 1.5))
                    intermediate_image = image.resize((intermediate_width, intermediate_height), Image.BICUBIC)
                    # Segundo paso: ajuste fino con LANCZOS
                    resized_image = intermediate_image.resize((new_width, new_height), resizing_algorithm)
                    logger.info(f"Redimensionamiento en dos pasos: {width}x{height} -> {intermediate_width}x{intermediate_height} -> {new_width}x{new_height}")
                else:
                    # Redimensionamiento directo para imágenes no tan grandes
                    resized_image = image.resize((new_width, new_height), resizing_algorithm)
                    logger.info(f"Redimensionamiento directo: {width}x{height} -> {new_width}x{new_height}")
            else:
                # Redimensionamiento estándar
                resized_image = image.resize((new_width, new_height), Image.LANCZOS)
                logger.info(f"Redimensionamiento estándar: {width}x{height} -> {new_width}x{new_height}")
            
            # Determinar formato de salida óptimo basado en el contenido de la imagen
            output_format = "JPEG"  # Formato predeterminado
            
            # Verificar si la imagen tiene transparencia (canal alfa)
            if image.mode == 'RGBA' or image.mode == 'LA' or (image.mode == 'P' and 'transparency' in image.info):
                logger.info("Imagen con transparencia detectada, usando formato PNG")
                output_format = "PNG"
            else:
                # Para imágenes sin transparencia, JPEG es más eficiente
                output_format = "JPEG"
            
            # Convertir la imagen redimensionada a bytes con optimización
            output_buffer = io.BytesIO()
            
            if output_format == "JPEG":
                # Comprimir con calidad progresiva si es necesario
                quality = 95  # Calidad inicial
                resized_image.save(output_buffer, format=output_format, quality=quality, optimize=True)
                compressed_data = output_buffer.getvalue()
                compressed_size_mb = len(compressed_data) / (1024 * 1024)
                
                # Reducir la calidad progresivamente si es necesario
                while compressed_size_mb > max_size_mb and quality > 30:
                    quality -= 5
                    output_buffer = io.BytesIO()
                    resized_image.save(output_buffer, format=output_format, quality=quality, optimize=True)
                    compressed_data = output_buffer.getvalue()
                    compressed_size_mb = len(compressed_data) / (1024 * 1024)
                    logger.info(f"Comprimiendo imagen con calidad {quality}, tamaño: {compressed_size_mb:.2f}MB")
                    
                return output_buffer.getvalue()
            else:  # PNG
                # Intentar optimizar PNG
                resized_image.save(output_buffer, format=output_format, optimize=True)
                compressed_data = output_buffer.getvalue()
                compressed_size_mb = len(compressed_data) / (1024 * 1024)
                
                # Si el PNG sigue siendo demasiado grande, convertir a JPEG si es posible
                if compressed_size_mb > max_size_mb:
                    logger.info("PNG demasiado grande después de optimización, intentando convertir a JPEG")
                    # Convertir a RGB si tiene canal alfa
                    if resized_image.mode == 'RGBA':
                        # Crear un fondo blanco y componer la imagen sobre él
                        background = Image.new('RGB', resized_image.size, (255, 255, 255))
                        background.paste(resized_image, mask=resized_image.split()[3])  # 3 es el canal alfa
                        resized_image = background
                    elif resized_image.mode != 'RGB':
                        resized_image = resized_image.convert('RGB')
                    
                    # Guardar como JPEG con compresión progresiva
                    output_format = "JPEG"
                    quality = 95
                    output_buffer = io.BytesIO()
                    resized_image.save(output_buffer, format=output_format, quality=quality, optimize=True)
                    compressed_data = output_buffer.getvalue()
                    compressed_size_mb = len(compressed_data) / (1024 * 1024)
                    
                    # Reducir calidad si es necesario
                    while compressed_size_mb > max_size_mb and quality > 30:
                        quality -= 5
                        output_buffer = io.BytesIO()
                        resized_image.save(output_buffer, format=output_format, quality=quality, optimize=True)
                        compressed_data = output_buffer.getvalue()
                        compressed_size_mb = len(compressed_data) / (1024 * 1024)
                        logger.info(f"Comprimiendo imagen convertida a JPEG con calidad {quality}, tamaño: {compressed_size_mb:.2f}MB")
                
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


# Funciones para la gestión de archivos temporales
def get_file_age_hours(filepath: str) -> float:
    """
    Calcula la antigüedad de un archivo en horas.
    
    Args:
        filepath (str): Ruta al archivo.
        
    Returns:
        float: Antigüedad del archivo en horas.
    """
    try:
        # Obtener tiempo de modificación del archivo
        mtime = os.path.getmtime(filepath)
        # Calcular diferencia con tiempo actual
        age_seconds = time.time() - mtime
        # Convertir a horas
        age_hours = age_seconds / 3600
        return age_hours
    except Exception as e:
        logger.error(f"Error al calcular la antigüedad del archivo {filepath}: {str(e)}")
        logger.exception("Detalles del error:")
        return 0.0

def cleanup_old_temp_images(directory: str = "temp_images", hours_threshold: float = 24.0) -> Tuple[int, List[str]]:
    """
    Limpia archivos de imágenes temporales que superan un umbral de antigüedad.
    
    Args:
        directory (str): Directorio donde se encuentran los archivos temporales.
        hours_threshold (float): Umbral de antigüedad en horas para eliminar archivos.
        
    Returns:
        tuple: (int, list) - Número de archivos eliminados y lista de rutas eliminadas.
    """
    try:
        if not os.path.exists(directory):
            logger.info(f"El directorio {directory} no existe. No hay archivos para limpiar.")
            return 0, []
        
        # Obtener todos los archivos en el directorio
        file_pattern = os.path.join(directory, "*")
        all_files = glob.glob(file_pattern)
        
        # Filtrar archivos por antigüedad
        files_to_delete = []
        for filepath in all_files:
            if os.path.isfile(filepath):  # Asegurarse de que es un archivo, no un directorio
                age_hours = get_file_age_hours(filepath)
                if age_hours >= hours_threshold:
                    files_to_delete.append(filepath)
        
        # Eliminar archivos antiguos
        deleted_count = 0
        deleted_files = []
        for filepath in files_to_delete:
            try:
                os.remove(filepath)
                deleted_count += 1
                deleted_files.append(filepath)
                logger.info(f"Archivo temporal eliminado: {filepath} (antigüedad: {get_file_age_hours(filepath):.2f} horas)")
            except Exception as e:
                logger.error(f"Error al eliminar archivo temporal {filepath}: {str(e)}")
        
        if deleted_count > 0:
            logger.info(f"Se eliminaron {deleted_count} archivos temporales con antigüedad mayor a {hours_threshold} horas")
        else:
            logger.info(f"No se encontraron archivos temporales con antigüedad mayor a {hours_threshold} horas")
        
        return deleted_count, deleted_files
    
    except Exception as e:
        logger.error(f"Error al limpiar archivos temporales: {str(e)}")
        logger.exception("Detalles del error:")
        return 0, []

# Funciones auxiliares para facilitar el uso desde la interfaz
def resize_image(image_path, max_pixels=33177600, max_size_mb=4, preserve_content=True):
    """
    Redimensiona una imagen si excede el número máximo de píxeles o tamaño.
    Preserva la relación de aspecto y el contenido importante de la imagen.
    
    Args:
        image_path (str): Ruta al archivo de imagen.
        max_pixels (int): Número máximo de píxeles permitidos (33177600 para Groq).
        max_size_mb (int): Tamaño máximo en MB (4MB para imágenes base64 en Groq).
        preserve_content (bool): Si es True, intenta preservar el contenido importante al redimensionar.
        
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
        
        # Calcular dimensiones óptimas basadas en restricciones
        if needs_resize_pixels:
            # Calcular la relación de redimensionamiento por píxeles
            ratio_pixels = (max_pixels / current_pixels) ** 0.5
            new_width_pixels = int(width * ratio_pixels)
            new_height_pixels = int(height * ratio_pixels)
            logger.info(f"Redimensionamiento necesario por píxeles: {new_width_pixels}x{new_height_pixels}")
        else:
            new_width_pixels = width
            new_height_pixels = height
        
        # Si la imagen es muy grande en tamaño pero no en píxeles, estimar dimensiones
        if needs_resize_size and not needs_resize_pixels:
            # Estimar factor de reducción basado en tamaño
            size_ratio = max_size_mb / original_size_mb
            # Aplicar un factor de seguridad (0.8) para compensar la compresión
            pixel_ratio = (size_ratio * 0.8) ** 0.5
            new_width_pixels = int(width * pixel_ratio)
            new_height_pixels = int(height * pixel_ratio)
            logger.info(f"Redimensionamiento estimado por tamaño: {new_width_pixels}x{new_height_pixels}")
        
        # Redimensionar la imagen preservando contenido si es necesario
        if preserve_content and (width > 1000 or height > 1000):
            logger.info("Usando redimensionamiento inteligente para preservar contenido importante")
            # Usar un algoritmo de mejor calidad para imágenes grandes
            resizing_algorithm = Image.LANCZOS
            
            # Si la imagen es muy grande, usar un enfoque en dos pasos para mejor calidad
            if width > 3000 or height > 3000:
                # Primer paso: reducir a un tamaño intermedio
                intermediate_width = min(width, int(new_width_pixels * 1.5))
                intermediate_height = min(height, int(new_height_pixels * 1.5))
                intermediate_image = image.resize((intermediate_width, intermediate_height), Image.BICUBIC)
                # Segundo paso: ajuste fino con LANCZOS
                resized_image = intermediate_image.resize((new_width_pixels, new_height_pixels), resizing_algorithm)
                logger.info(f"Redimensionamiento en dos pasos: {width}x{height} -> {intermediate_width}x{intermediate_height} -> {new_width_pixels}x{new_height_pixels}")
            else:
                # Redimensionamiento directo para imágenes no tan grandes
                resized_image = image.resize((new_width_pixels, new_height_pixels), resizing_algorithm)
                logger.info(f"Redimensionamiento directo: {width}x{height} -> {new_width_pixels}x{new_height_pixels}")
        else:
            # Redimensionamiento estándar
            resized_image = image.resize((new_width_pixels, new_height_pixels), Image.LANCZOS)
            logger.info(f"Redimensionamiento estándar: {width}x{height} -> {new_width_pixels}x{new_height_pixels}")
        
        # Determinar formato de salida óptimo basado en el contenido de la imagen
        output_format = "JPEG"  # Formato predeterminado
        
        # Verificar si la imagen tiene transparencia (canal alfa)
        if image.mode == 'RGBA' or image.mode == 'LA' or (image.mode == 'P' and 'transparency' in image.info):
            logger.info("Imagen con transparencia detectada, usando formato PNG")
            output_format = "PNG"
            # Crear extensión basada en el formato
            extension = ".png"
        else:
            # Para imágenes sin transparencia, JPEG es más eficiente
            output_format = "JPEG"
            extension = ".jpg"
        
        # Comprimir la imagen si aún excede el tamaño máximo
        quality = 95  # Calidad inicial
        output_buffer = io.BytesIO()
        
        if output_format == "JPEG":
            resized_image.save(output_buffer, format=output_format, quality=quality, optimize=True)
        else:  # PNG
            resized_image.save(output_buffer, format=output_format, optimize=True)
            
        compressed_data = output_buffer.getvalue()
        compressed_size_mb = len(compressed_data) / (1024 * 1024)
        
        # Para JPEG, reducir la calidad progresivamente si es necesario
        if output_format == "JPEG":
            while compressed_size_mb > max_size_mb and quality > 30:
                quality -= 5
                output_buffer = io.BytesIO()
                resized_image.save(output_buffer, format=output_format, quality=quality, optimize=True)
                compressed_data = output_buffer.getvalue()
                compressed_size_mb = len(compressed_data) / (1024 * 1024)
                logger.info(f"Comprimiendo imagen con calidad {quality}, tamaño: {compressed_size_mb:.2f}MB")
        
        # Para PNG, si sigue siendo demasiado grande después de la optimización, convertir a JPEG si es posible
        if output_format == "PNG" and compressed_size_mb > max_size_mb:
            logger.info("PNG demasiado grande después de optimización, intentando convertir a JPEG")
            # Convertir a RGB si tiene canal alfa
            if resized_image.mode == 'RGBA':
                # Crear un fondo blanco y componer la imagen sobre él
                background = Image.new('RGB', resized_image.size, (255, 255, 255))
                background.paste(resized_image, mask=resized_image.split()[3])  # 3 es el canal alfa
                resized_image = background
            elif resized_image.mode != 'RGB':
                resized_image = resized_image.convert('RGB')
                
            # Guardar como JPEG con compresión progresiva
            output_format = "JPEG"
            extension = ".jpg"
            quality = 95
            output_buffer = io.BytesIO()
            resized_image.save(output_buffer, format=output_format, quality=quality, optimize=True)
            compressed_data = output_buffer.getvalue()
            compressed_size_mb = len(compressed_data) / (1024 * 1024)
            
            # Reducir calidad si es necesario
            while compressed_size_mb > max_size_mb and quality > 30:
                quality -= 5
                output_buffer = io.BytesIO()
                resized_image.save(output_buffer, format=output_format, quality=quality, optimize=True)
                compressed_data = output_buffer.getvalue()
                compressed_size_mb = len(compressed_data) / (1024 * 1024)
                logger.info(f"Comprimiendo imagen convertida a JPEG con calidad {quality}, tamaño: {compressed_size_mb:.2f}MB")
        
        # Guardar la imagen redimensionada/comprimida
        resized_path = f"{os.path.splitext(image_path)[0]}_optimized{extension}"
        with open(resized_path, "wb") as f:
            f.write(compressed_data)
        
        # Verificar dimensiones finales
        final_image = Image.open(io.BytesIO(compressed_data))
        final_width, final_height = final_image.size
        final_pixels = final_width * final_height
        
        logger.info(f"Imagen optimizada guardada en {resized_path}")
        logger.info(f"Dimensiones finales: {final_width}x{final_height} = {final_pixels} píxeles")
        logger.info(f"Tamaño final: {compressed_size_mb:.2f}MB")
        logger.info(f"Formato final: {output_format}, Calidad: {quality if output_format == 'JPEG' else 'N/A'}")
        
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


def check_and_cleanup_temp_images(directory="temp_images", hours_threshold=24.0):
    """
    Verifica y limpia imágenes temporales antiguas al iniciar la aplicación.
    Esta función está diseñada para ser llamada durante el inicio de la aplicación.
    
    Args:
        directory (str): Directorio donde se almacenan las imágenes temporales.
        hours_threshold (float): Antigüedad en horas para considerar un archivo como obsoleto.
        
    Returns:
        tuple: (int, list) - Número de archivos eliminados y lista de rutas eliminadas.
    """
    try:
        logger.info(f"Verificando archivos temporales en '{directory}' con antigüedad mayor a {hours_threshold} horas...")
        
        # Ejecutar la limpieza de archivos temporales
        deleted_count, deleted_files = cleanup_old_temp_images(directory, hours_threshold)
        
        # Registrar resultado
        if deleted_count > 0:
            logger.info(f"Limpieza completada: {deleted_count} archivos eliminados")
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Hora de limpieza: {current_time}")
        else:
            logger.info("No se encontraron archivos temporales para eliminar")
            
        return deleted_count, deleted_files
        
    except Exception as e:
        logger.error(f"Error durante la verificación y limpieza de archivos temporales: {str(e)}")
        logger.exception("Detalles del error:")
        return 0, []
