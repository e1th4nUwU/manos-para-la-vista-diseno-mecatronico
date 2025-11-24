import os
import asyncio
from dotenv import load_dotenv
from telegram import Bot
from datetime import datetime
from telegram.request import HTTPXRequest
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfgen import canvas

# Load environment variables from .env file
load_dotenv('src/.env')

# Get environment variable from .env
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
ENV = os.getenv("ENV", "development")


# Initialize the Telegram bot
TELEGRAM_REQUEST = HTTPXRequest(connection_pool_size=10)
TELEGRAM_BOT = Bot(token=TELEGRAM_BOT_TOKEN,request=TELEGRAM_REQUEST)


class NotificationService:
    """
    This is a base class for notifications.
    
    Methods:
    --------
    send(message: str, options: dict = {}) -> bool: Sends a message to a Telegram chat.
    format_and_send_api_response(league:str, data: dict, options: dict = {}) -> bool: Formats a JSON object and sends it to a chat.
    """
    @staticmethod
    async def send(message):
        """
        Sends a message to a chat.
        
        Args:
            message (str): The message to be sent.
            options (dict): The options for the message.
        """
        pass
    
    @classmethod
    async def format_and_send_api_response(cls,league:str, data: dict):
        """
        Formats a JSON object and sends it to a Telegram chat.
        
        Args:
            data (dict): The JSON object to be formatted and sent.
            options (dict): The options for the message.
        """
        try:
            
            message = f"{league}"
            # Add Emoji
            match(league):
                case "MLB":
                    message = f"{league} ⚾️ :: "
                case "NBA":
                    message = f"{league} 🏀 :: "
                case "NFL":
                    message = f"{league} 🏈 :: "
                case "NHL":
                    message = f"{league} 🏒 :: "
            if "Load" in data:
                print("\tLoad pipeline: ", data['Load'])
                try:
                    message += f"Evento Load terminado a las _{datetime.now().strftime('%H:%M:%S')}_"
                    print("\tLoad responses: ", data['Load'])
                    if data['Load']['events'].get("code") == 404:
                        message += f"\n{data['Load']['events']['exit-message']}"
                        await cls.send(message)
                        return
                    
                    append = f"\nSe acaban de insertar {data['Load']['events']["Events"]['new-matches']} matches de los {data['Load']['events']["Events"]['found-matches']+data['Load']['events']['new-matches']} que tenemos en la BD para la jornada de hoy"
                    append += f"\nSe insertaron {data['Load']['projections']["Projections"]['found-players']} de las {data['Load']['projections']["Projections"]['found-players'] + data['Load']['projections']["Projections"]['not-found-players']} proyecciones desde Rotowire"
                    append += f"\nSe encontraron {data['Load']['injuries']["Injuries"]['found-injuries']} injuries para hoy de las {data['Load']['injuries']["Injuries"]['found-injuries'] + data['Load']['injuries']["Injuries"]['not-found-injuries']} totales de Rotowire"
                    append += f"\nSe upsertearon {data['Load']['props']["Props"]['found-props']} de las {data['Load']['props']["Props"]['found-props'] + data['Load']['props']["Props"]['not-found-props']} props disponibles en DraftKings"
                    
                    if "batterVsPitcher" in data['Load']:
                        append += f"\nSe actualizaron {data['Load']['batterVsPitcher']['found-teams']} equipos y {data['Load']['batterVsPitcher']['found-matches']} matches"
                    if "teamRankingsByPosition" in data['Load']:
                        append += f"\nSe actualizaron {data['Load']['teamRankingsByPosition']['found-rankings']} rankings de posiciones de equipos"
                    message += append
                    
                except:
                    message += f"Evento Load terminó con detalles, revisar logs @everyone ({datetime.now().strftime('%H:%M:%S')})"
            
            if "Results" in data:
                print("\tEvento Results terminado a las _", datetime.now().strftime('%H:%M:%S'), "_")
                print("\tResults pipeline: ", data['Results'])
                try:
                    message += f"\nSe actualizaron {data['Results']['gamelogs']['Gamelogs']['gamelogs']} gamelogs y el boxscore de {data['Results']['gamelogs']['Gamelogs']['analyses']} análisis"
                    message += f"\nSe actualizaron standings de {data['Results']['standings']['Standings']["found-teams"]} de {data['Results']['standings']['Standings']["found-teams"] + data['Results']['standings']['Standings']['missing-teams']} los equipos encontrados"
                    message += f"\nSe actualizaron stats y rankings de {data['Results']['teamStatsAndRankings']['TeamStatsAndRankings']['found-teams']} equipos"
                    message += f"\nSe actualizaron {data['Results']['playerStatsAndRankings']['PlayerStatsAndRankings']['found-players']} jugadores"
                except:
                    message = f"Evento Results terminó con detalles, revisar logs @everyone ({datetime.now().strftime('%H:%M:%S')})"
            
            if "Events" in data:
                print("\tEvents pipeline: ", data['Events'])
                try:
                    message += f"Se acaban de insertar {data['Events']['new-matches']} matches de los {data['Events']['found-matches']+data['Events']['new-matches']} que tenemos en la BD para la jornada de hoy"
                except:
                    message += f"Evento Events: {data['Events']['exit-message']}"
            if "Projections" in data:
                print("\tProjections response: ", data['Projections'])
                try:
                    message += f"Se insertaron {data['Projections']['found-players']} de {data['Projections']['found-players'] + data['Projections']['not-found-players']} proyecciones desde Rotowire"
                except:
                    message += f"Evento Projections: {data['Projections']['exit-message']}"
                    
            if "Injuries" in data:
                print("\tInjuries response: ", data['Injuries'])
                try:
                    message += f"Se encontraron {data['Injuries']['found-injuries']} injuries para hoy de las {data['Injuries']['found-injuries'] + data['Injuries']['not-found-injuries']} totales de Rotowire"
                except:
                    message += f"Evento Injuries: {data['Injuries']['exit-message']}"
            if "Props" in data:
                print("\tProps response: ", data['Props'])
                try:
                    message += f"Se upsertearon {data['Props']['found-props']} de {data['Props']['found-props'] + data['Props']['not-found-props']} props disponibles en DraftKings"
                except:
                    message += f"Evento Props: {data['Props']['exit-message']}"
            
            if "TeamsStatsMLB" in data:
                print("\tTeamsStatsMLB response: ", data['TeamsStatsMLB'])
                try:
                    message += f"Se actualizaron stats {data['TeamsStatsMLB']['found-batting']} (B) y {data['TeamsStatsMLB']['found-pitching']} (P) equipos"
                except:
                    message += f"Evento TeamsStats: {data['TeamsStatsMLB']['exit-message']}"
                    
            if "TeamsRankingsMLB" in data:
                print("\tTeamsRankingsMLB response: ", data['TeamsRankingsMLB'])
                try:
                    message += f"Se actualizaron rankings {data['TeamsRankingsMLB']['found-batting']} (B) y {data['TeamsRankingsMLB']['found-pitching']} (P) equipos"
                except:
                    message += f"Evento TeamsRankings: {data['TeamsRankingsMLB']['exit-message']}"
            
            if "BatterVsPitcher" in data:
                print("\tBatterVsPitcher response: ", data['BatterVsPitcher'])
                try:
                    message += f"Se actualizaron {data['BatterVsPitcher']['found-teams']} equipos y {data['BatterVsPitcher']['found-matches']} matches"
                except:
                    message += f"Evento BatterVsPitcher: {data['BatterVsPitcher']['exit-message']}"
            
            if "PlayerStatsAndRankings" in data:
                print("\tPlayerStatsAndRankings response: ", data['PlayerStatsAndRankings'])
                try:
                    message += f"Se actualizaron {data['PlayerStatsAndRankings']['found-players']} jugadores y {data['PlayerStatsAndRankings']['found-teams']} equipos"
                except:
                    message += f"Evento PlayerStatsAndRankings: {data['PlayerStatsAndRankings']['exit-message']}"
            
            if "TeamStatsAndRankings" in data:
                print("\tTeamStatsAndRankings response: ", data['TeamStatsAndRankings'])
                try:
                    message += f"Se actualizaron stats y rankings de {data['TeamStatsAndRankings']['found-teams']} equipos"
                except:
                    message += f"Evento TeamsStats: {data['TeamStatsAndRankings']['exit-message']}"
            
            if "Gamelogs" in data:
                print("\tGamelogs response: ", data['Gamelogs'])
                try:
                    message += f"Se actualizaron {data['Gamelogs']['gamelogs']} gamelogs y el boxscore de {data['Gamelogs']['analyses']} análisis"
                except:
                    message += f"Evento Gamelogs: {data['Gamelogs']['exit-message']}"
                    
            if "Standings" in data:
                print("\tStandings response: ", data['Standings'])
                try:
                    message += f"Se actualizaron standings de {data['Standings']['found-teams']} de {data['Standings']['found-teams'] + data['Standings']['missing-teams']} los equipos encontrados"
                except:
                    message += f"Evento Standings: {data['Standings']['exit-message']}\n\n"
                    
                    
            if "NRFI" in data:
                print("\tNRFI response: ", data['NRFI'])
                try:
                    message += f"NRFI: Lineups actualizados: {data['NRFI']['lineups']}, Matches actualizados: {data['NRFI']['matches']}"
                except:
                    message += f"Evento NRFI: {data['NRFI']['exit-message']}"
            
            if "Analysis" in data:
                print("\tAnalysis response: ", data['Analysis'])
                try:
                    message += f"Se insertaron {data['Analysis']['successful']} de {data['Analysis']['successful'] + data['Analysis']['failed']} props en la BD"
                except:
                    message += f"Evento Analysis: {data['Analysis']['exit-message']}"
            
            if "Strategies" in data:
                print("\tStrategies response: ", data['Strategies'])
                try:
                    message += f"{data['Strategies']['count']} estrategias actualizadas"
                except:
                    message += f"Evento Strategies: {data['Strategies']['exit-message']}"
            
            if "InsertMongoAnalysis" in data:
                print("\tInsertMongoAnalysis response: ", data['InsertMongoAnalysis'])
                try:    
                    if data['InsertMongoAnalysis'].get('end_date'):
                        message += f"Se insertaron {data['InsertMongoAnalysis']['rows']} análisis desde Mongo a Bigquery ({data['InsertMongoAnalysis']['start_date']} - {data['InsertMongoAnalysis']['end_date']})"
                    elif data['InsertMongoAnalysis'].get('start_date'):
                        message += f"Se insertaron {data['InsertMongoAnalysis']['rows']} análisis desde Mongo a Bigquery ({data['InsertMongoAnalysis']['start_date']})"
                    else:
                        message += f"Se insertaron {data['InsertMongoAnalysis']['rows']} análisis desde Mongo a Bigquery (scrapingId: {data['InsertMongoAnalysis']['scrapingId']})"
                except:
                    message += f"InsertMongoAnalysis: {data['InsertMongoAnalysis']['exit-message']}"
            
            if "StrategiesParquet" in data:
                print("\tStrategiesParquet response: ", data['StrategiesParquet'])
                
                try:
                    message += f"Parquet de estrategias creado con {data['StrategiesParquet']['count']} análisis"
                except:
                    message += f"StrategiesParquet: {data['StrategiesParquet']['exit-message']}"
            
            if "GPTPredictions" in data:
                print("\tGPTPredictions response: ", data['GPTPredictions'])
                try:
                    message += f"Inserciones de GPT: {data['GPTPredictions']['insertions']}"
                except:
                    message += f"GPTPredictions: {data['GPTPredictions']['exit-message']}\n\n"
                    
            if "MatchSchedule" in data:
                print("\tMatchSchedule response: ", data['MatchSchedule'])
                try:
                    message += f"Se encontraron {data['MatchSchedule']['matches']} partidos hoy y se programaron {data['MatchSchedule']['gcp_tasks']} ejecuciones del live"
                except:
                    message += f"MatchSchedule: {data['MatchSchedule']['exit-message']}"
                    
            if "TeamRankingsByPosition" in data:
                print("\tTeamRankingsByPosition response: ", data['TeamRankingsByPosition'])
                try:
                    message += f"Se actualizaron {data['TeamRankingsByPosition']['found-rankings']} rankings de posiciones de equipos"
                except:
                    message += f"TeamRankingsByPosition: {data['TeamRankingsByPosition']['exit-message']}"
                
            if "message" in data:
                message += f"{data['message']}"

            # Use child class notification method (Telegram, Discord, etc.)
            await cls.send(message)
            
        except Exception as e:
            print(e)

# Define the Telegram class
class Telegram(NotificationService):
    """
    This class contains methods for sending messages to a Telegram chat.
    
    Methods:
    --------
    send(message: str, options: dict = {}) -> bool: Sends a message to a Telegram chat.
    """
    @staticmethod
    async def send(message: str):
        """
        Sends a message to a Telegram chat.
        
        Args:
            message (str): The message to be sent.
            options (dict): The options for the message.
        """
        try:
            chat_id = TELEGRAM_CHAT_ID
            if ENV == 'production':
                await TELEGRAM_BOT.send_message(chat_id, message)
            return True
        except Exception as e:
            print(e)
            return False
    
    @staticmethod
    async def send_document(file_path: str, caption: str = ""):
        """
        Sends a document (PDF) to a Telegram chat.
        
        Args:
            file_path (str): Path to the document file.
            caption (str): Optional caption for the document.
        """
        try:
            chat_id = TELEGRAM_CHAT_ID
            if ENV == 'production':
                with open(file_path, 'rb') as document:
                    await TELEGRAM_BOT.send_document(
                        chat_id=chat_id,
                        document=document,
                        caption=caption
                    )
            else:
                print(f"[DEV MODE] Would send document: {file_path}")
                print(f"[DEV MODE] Caption: {caption}")
            return True
        except Exception as e:
            print(f"Error sending document: {e}")
            return False


class DaltonismReportGenerator:
    """
    Generates PDF reports for Daltonism test results.
    """
    
    @staticmethod
    def generate_pdf_report(test_results: dict, output_path: str = None):
        """
        Generates a PDF report with the test results.
        
        Args:
            test_results (dict): Dictionary containing test results with keys:
                - color_score: int
                - color_attempts: int
                - ishihara_score: int
                - ishihara_attempts: int
                - timestamp: str (optional)
                - patient_id: str (optional)
            output_path (str): Path where to save the PDF. If None, saves to /tmp/
        
        Returns:
            str: Path to the generated PDF file
        """
        try:
            # Generate filename with timestamp
            timestamp = test_results.get('timestamp', datetime.now().strftime('%Y%m%d_%H%M%S'))
            if output_path is None:
                output_path = f"/tmp/daltonism_test_{timestamp}.pdf"
            
            # Create PDF document
            doc = SimpleDocTemplate(output_path, pagesize=letter)
            story = []
            styles = getSampleStyleSheet()
            
            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#2196F3'),
                spaceAfter=30,
                alignment=TA_CENTER
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=16,
                textColor=colors.HexColor('#FF5722'),
                spaceAfter=12,
                alignment=TA_LEFT
            )
            
            # Logo del proyecto (tamaño reducido para que quepa en una hoja)
            logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "img", "logo.png")
            if os.path.exists(logo_path):
                try:
                    logo = Image(logo_path, width=0.6*inch, height=0.6*inch)
                    logo.hAlign = 'CENTER'
                    story.append(logo)
                    story.append(Spacer(1, 0.05 * inch))
                except Exception as e:
                    print(f"[WARNING] No se pudo cargar el logo: {e}")
            
            # Title
            title = Paragraph("Reporte de Test de Daltonismo", title_style)
            story.append(title)
            story.append(Spacer(1, 0.1 * inch))
            
            # Test information
            info_data = [
                ['Fecha y Hora:', datetime.now().strftime('%d/%m/%Y %H:%M:%S')],
                ['ID Paciente:', test_results.get('patient_id', 'N/A')],
            ]
            
            info_table = Table(info_data, colWidths=[2*inch, 4*inch])
            info_table.setStyle(TableStyle([
                ('FONT', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 12),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#555555')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ]))
            
            story.append(info_table)
            story.append(Spacer(1, 0.15 * inch))
            
            # Results section
            results_heading = Paragraph("Resultados del Test", heading_style)
            story.append(results_heading)
            story.append(Spacer(1, 0.1 * inch))
            
            # Calculate percentages
            color_score = test_results.get('color_score', 0)
            color_attempts = test_results.get('color_attempts', 1)
            ishihara_score = test_results.get('ishihara_score', 0)
            ishihara_attempts = test_results.get('ishihara_attempts', 1)
            
            color_percentage = (color_score / color_attempts) * 100 if color_attempts > 0 else 0
            ishihara_percentage = (ishihara_score / ishihara_attempts) * 100 if ishihara_attempts > 0 else 0
            total_score = color_score + ishihara_score
            total_attempts = color_attempts + ishihara_attempts
            overall_percentage = (total_score / total_attempts) * 100 if total_attempts > 0 else 0
            
            # Results table
            results_data = [
                ['Test', 'Correctas', 'Total', 'Porcentaje'],
                ['Test de Colores', str(color_score), str(color_attempts), f'{color_percentage:.1f}%'],
                ['Test de Ishihara', str(ishihara_score), str(ishihara_attempts), f'{ishihara_percentage:.1f}%'],
                ['TOTAL', str(total_score), str(total_attempts), f'{overall_percentage:.1f}%'],
            ]
            
            results_table = Table(results_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
            results_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2196F3')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
                ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#E3F2FD')),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 11),
                ('TOPPADDING', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ]))
            
            story.append(results_table)
            story.append(Spacer(1, 0.4 * inch))
            
            # Evaluation
            evaluation_heading = Paragraph("Evaluación", heading_style)
            story.append(evaluation_heading)
            story.append(Spacer(1, 0.1 * inch))
            
            if overall_percentage >= 85:
                evaluation = "Visión cromática normal"
                eval_color = colors.HexColor('#4CAF50')
                recommendation = "No se detectaron indicios de deficiencia en la visión de colores."
            elif overall_percentage >= 65:
                evaluation = "Posible deficiencia leve"
                eval_color = colors.HexColor('#FF9800')
                recommendation = "Se recomienda realizar un seguimiento y consulta con un especialista si persisten las dificultades."
            else:
                evaluation = "Se recomienda consulta oftalmológica"
                eval_color = colors.HexColor('#F44336')
                recommendation = "Los resultados sugieren una posible deficiencia en la visión de colores. Se recomienda consultar con un oftalmólogo para una evaluación más detallada."
            
            eval_style = ParagraphStyle(
                'EvalStyle',
                parent=styles['Normal'],
                fontSize=14,
                textColor=eval_color,
                spaceAfter=12,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            )
            
            recommendation_style = ParagraphStyle(
                'RecommendationStyle',
                parent=styles['Normal'],
                fontSize=12,
                spaceAfter=12,
                alignment=TA_LEFT
            )
            
            eval_para = Paragraph(evaluation, eval_style)
            story.append(eval_para)
            story.append(Spacer(1, 0.2 * inch))
            
            recommendation_para = Paragraph(f"<b>Recomendación:</b> {recommendation}", recommendation_style)
            story.append(recommendation_para)
            
            # Footer
            story.append(Spacer(1, 0.5 * inch))
            footer_style = ParagraphStyle(
                'FooterStyle',
                parent=styles['Normal'],
                fontSize=9,
                textColor=colors.grey,
                alignment=TA_CENTER
            )
            footer = Paragraph(
                "Este reporte es generado automáticamente por el sistema de Test de Daltonismo.<br/>"
                "Para diagnóstico médico oficial, consulte con un oftalmólogo certificado.",
                footer_style
            )
            story.append(footer)
            
            # Build PDF
            doc.build(story)
            print(f"[PDF] Reporte generado: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"[ERROR] Error generando PDF: {e}")
            return None
    
    @staticmethod
    async def generate_and_send_report(test_results: dict):
        """
        Generates a PDF report and sends it to Telegram.
        
        Args:
            test_results (dict): Dictionary containing test results
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Generate PDF
            pdf_path = DaltonismReportGenerator.generate_pdf_report(test_results)
            
            if pdf_path is None:
                print("[ERROR] No se pudo generar el PDF")
                return False
            
            # Calculate overall percentage for caption
            total_score = test_results.get('color_score', 0) + test_results.get('ishihara_score', 0)
            total_attempts = test_results.get('color_attempts', 1) + test_results.get('ishihara_attempts', 1)
            overall_percentage = (total_score / total_attempts) * 100 if total_attempts > 0 else 0
            
            # Create caption
            caption = (
                f"📊 Nuevo resultado de Test de Daltonismo\n"
                f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
                f"📈 Puntuación: {total_score}/{total_attempts} ({overall_percentage:.1f}%)\n"
                f"👤 ID: {test_results.get('patient_id', 'N/A')}"
            )
            
            # Send to Telegram
            success = await Telegram.send_document(pdf_path, caption)
            
            # Clean up temporary file
            try:
                if os.path.exists(pdf_path):
                    os.remove(pdf_path)
                    print(f"[PDF] Archivo temporal eliminado: {pdf_path}")
            except Exception as e:
                print(f"[WARNING] No se pudo eliminar archivo temporal: {e}")
            
            return success
            
        except Exception as e:
            print(f"[ERROR] Error en generate_and_send_report: {e}")
            return False
