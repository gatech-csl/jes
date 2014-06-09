  /*
   * conversion tools from tritonus (http://www.tritonus.org)
   */
  
  /*
   *      TConversionTool.java
   */ 
  
  /*
   *  Copyright (c) 1999,2000 by Florian Bomers <florian@bome.com>
   *  Copyright (c) 2000 by Matthias Pfisterer <matthias.pfisterer@gmx.de>
   *
   *
   *   This program is free software; you can redistribute it and/or modify
   *   it under the terms of the GNU Library General Public License as 
   *   published by the Free Software Foundation; either version 2 of the 
   *   License, or (at your option) any later version.
   *
   *   This program is distributed in the hope that it will be useful,
   *   but WITHOUT ANY WARRANTY; without even the implied warranty of
   *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   *   GNU Library General Public License for more details.
   *
   *   You should have received a copy of the GNU Library General Public
   *   License along with this program; if not, write to the Free Software
   *   Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
   *
   */
public class TConversionTool 
{
  
  /**
   * Converts 2 successive bytes starting at <code>byteOffset</code> in 
   * <code>buffer</code> to a signed integer sample with 16bit range.
   * <p>
   * For little endian, buffer[byteOffset] is interpreted as low byte,
   * whereas it is interpreted as high byte in big endian.
   * <p> This is a reference function.
   */ 
  public static int bytesToInt16( byte [] buffer, int byteOffset, 
                                  boolean bigEndian) 
  { 
    return bigEndian?
      ((buffer[byteOffset]<<8) | (buffer[byteOffset+1] & 0xFF)):
      
      ((buffer[byteOffset+1]<<8) | (buffer[byteOffset] & 0xFF));
  } 
  
  /**
   * Converts 3 successive bytes starting at <code>byteOffset</code> in 
   * <code>buffer</code> to a signed integer sample with 24bit range.
   * <p>
   * For little endian, buffer[byteOffset] is interpreted as lowest byte,
   * whereas it is interpreted as highest byte in big endian.
   * <p> This is a reference function.
   */ 
  public static int bytesToInt24( byte [] buffer, int byteOffset, 
                                  boolean bigEndian) 
  { 
    return bigEndian?
      ((buffer[byteOffset]<<16) // let Java handle sign-bit 
         | ((buffer[byteOffset+1] & 0xFF)<<8) // inhibit sign-bit handling 
         | ((buffer[byteOffset+2] & 0xFF))):
      
      ((buffer[byteOffset+2]<<16) // let Java handle sign-bit 
         | ((buffer[byteOffset+1] & 0xFF)<<8) // inhibit sign-bit handling 
         | (buffer[byteOffset] & 0xFF));
  } 
  
  /**
   * Converts a 4 successive bytes starting at <code>byteOffset</code> in 
   * <code>buffer</code> to a signed 32bit integer sample.
   * <p>
   * For little endian, buffer[byteOffset] is interpreted as lowest byte,
   * whereas it is interpreted as highest byte in big endian.
   * <p> This is a reference function.
   */ 
  public static int bytesToInt32( byte [] buffer, int byteOffset, 
                                  boolean bigEndian) 
  { 
    return bigEndian?
      ((buffer[byteOffset]<<24) // let Java handle sign-bit 
         | ((buffer[byteOffset+1] & 0xFF)<<16) // inhibit sign-bit handling 
         | ((buffer[byteOffset+2] & 0xFF)<<8) // inhibit sign-bit handling 
         | (buffer[byteOffset+3] & 0xFF)):
      
      ((buffer[byteOffset+3]<<24) // let Java handle sign-bit 
         | ((buffer[byteOffset+2] & 0xFF)<<16) // inhibit sign-bit handling 
         | ((buffer[byteOffset+1] & 0xFF)<<8) // inhibit sign-bit handling 
         | (buffer[byteOffset] & 0xFF));
  } 
  
  /////////////////////// ULAW ///////////////////////////////////////////
  
  private static final boolean ZEROTRAP=true;
  private static final short BIAS=0x84;
  private static final int CLIP=32635;
  private static final int exp_lut1[] ={
    0,0,1,1,2,2,2,2,3,3,3,3,3,3,3,3,
    4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,
    5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,
    5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,
    6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,
    6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,
    6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,
    6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,
    7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,
    7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,
    7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,
    7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,
    7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,
    7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,
    7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,
    7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7
  };
  
  
  /* u-law to linear conversion table */ 
  private static short [] u2l = {
    -32124, -31100, -30076, -29052, -28028, -27004, -25980, -24956,
    -23932, -22908, -21884, -20860, -19836, -18812, -17788, -16764,
    -15996, -15484, -14972, -14460, -13948, -13436, -12924, -12412,
    -11900, -11388, -10876, -10364, -9852, -9340, -8828, -8316,
    -7932, -7676, -7420, -7164, -6908, -6652, -6396, -6140,
    -5884, -5628, -5372, -5116, -4860, -4604, -4348, -4092,
    -3900, -3772, -3644, -3516, -3388, -3260, -3132, -3004,
    -2876, -2748, -2620, -2492, -2364, -2236, -2108, -1980,
    -1884, -1820, -1756, -1692, -1628, -1564, -1500, -1436,
    -1372, -1308, -1244, -1180, -1116, -1052, -988, -924,
    -876, -844, -812, -780, -748, -716, -684, -652,
    -620, -588, -556, -524, -492, -460, -428, -396,
    -372, -356, -340, -324, -308, -292, -276, -260,
    -244, -228, -212, -196, -180, -164, -148, -132,
    -120, -112, -104, -96, -88, -80, -72, -64,
    -56, -48, -40, -32, -24, -16, -8, 0,
    32124, 31100, 30076, 29052, 28028, 27004, 25980, 24956,
    23932, 22908, 21884, 20860, 19836, 18812, 17788, 16764,
    15996, 15484, 14972, 14460, 13948, 13436, 12924, 12412,
    11900, 11388, 10876, 10364, 9852, 9340, 8828, 8316,
    7932, 7676, 7420, 7164, 6908, 6652, 6396, 6140,
    5884, 5628, 5372, 5116, 4860, 4604, 4348, 4092,
    3900, 3772, 3644, 3516, 3388, 3260, 3132, 3004,
    2876, 2748, 2620, 2492, 2364, 2236, 2108, 1980,
    1884, 1820, 1756, 1692, 1628, 1564, 1500, 1436,
    1372, 1308, 1244, 1180, 1116, 1052, 988, 924,
    876, 844, 812, 780, 748, 716, 684, 652,
    620, 588, 556, 524, 492, 460, 428, 396,
    372, 356, 340, 324, 308, 292, 276, 260,
    244, 228, 212, 196, 180, 164, 148, 132,
    120, 112, 104, 96, 88, 80, 72, 64,
    56, 48, 40, 32, 24, 16, 8, 0
  }; 
  public static short ulaw2linear( byte ulawbyte) 
  { 
    return u2l[ulawbyte & 0xFF];
  } 
  
  /**
   * Converts a linear signed 16bit sample to a uLaw byte.
   * Ported to Java by fb.
   * <BR>Originally by:<BR>
   * Craig Reese: IDA/Supercomputing Research Center <BR>
   * Joe Campbell: Department of Defense <BR>
   * 29 September 1989 <BR>
   */
  public static byte linear2ulaw(int sample) {
    int sign, exponent, mantissa, ulawbyte;
    
    if (sample>32767) sample=32767;
    else if (sample<-32768) sample=-32768;
    /* Get the sample into sign-magnitude. */
    sign = (sample >> 8) & 0x80;    /* set aside the sign */
    if (sign != 0) sample = -sample;    /* get magnitude */
    if (sample > CLIP) sample = CLIP;    /* clip the magnitude */
    
    /* Convert from 16 bit linear to ulaw. */
    sample = sample + BIAS;
    exponent = exp_lut1[(sample >> 7) & 0xFF];
    mantissa = (sample >> (exponent + 3)) & 0x0F;
    ulawbyte = ~(sign | (exponent << 4) | mantissa);
    if (ZEROTRAP)
      if (ulawbyte == 0) ulawbyte = 0x02;  /* optional CCITT trap */
    return((byte) ulawbyte);
  }
  
  
  /*
   * This source code is a product of Sun Microsystems, Inc. and is provided
   * for unrestricted use.  Users may copy or modify this source code without
   * charge.
   *
   * linear2alaw() - Convert a 16-bit linear PCM value to 8-bit A-law
   *
   * linear2alaw() accepts an 16-bit integer and encodes it as A-law data.
   *
   *              Linear Input Code       Compressed Code
   *      ------------------------        ---------------
   *      0000000wxyza                    000wxyz
   *      0000001wxyza                    001wxyz
   *      000001wxyzab                    010wxyz
   *      00001wxyzabc                    011wxyz
   *      0001wxyzabcd                    100wxyz
   *      001wxyzabcde                    101wxyz
   *      01wxyzabcdef                    110wxyz
   *      1wxyzabcdefg                    111wxyz
   *
   * For further information see John C. Bellamy's Digital Telephony, 1982,
   * John Wiley & Sons, pps 98-111 and 472-476.
   */ 
  private static final byte QUANT_MASK = 0xf; /* Quantization field mask. */
  private static final byte SEG_SHIFT = 4;  /* Left shift for segment number. */
  private static final short[] seg_end = {
    0xFF, 0x1FF, 0x3FF, 0x7FF, 0xFFF, 0x1FFF, 0x3FFF, 0x7FFF
  };
  
  
  /*
   * conversion table alaw to linear
   */
  private static short [] a2l = {
    -5504, -5248, -6016, -5760, -4480, -4224, -4992, -4736,
    -7552, -7296, -8064, -7808, -6528, -6272, -7040, -6784,
    -2752, -2624, -3008, -2880, -2240, -2112, -2496, -2368,
    -3776, -3648, -4032, -3904, -3264, -3136, -3520, -3392,
    -22016, -20992, -24064, -23040, -17920, -16896, -19968, -18944,
    -30208, -29184, -32256, -31232, -26112, -25088, -28160, -27136,
    -11008, -10496, -12032, -11520, -8960, -8448, -9984, -9472,
    -15104, -14592, -16128, -15616, -13056, -12544, -14080, -13568,
    -344, -328, -376, -360, -280, -264, -312, -296,
    -472, -456, -504, -488, -408, -392, -440, -424,
    -88, -72, -120, -104, -24, -8, -56, -40,
    -216, -200, -248, -232, -152, -136, -184, -168,
    -1376, -1312, -1504, -1440, -1120, -1056, -1248, -1184,
    -1888, -1824, -2016, -1952, -1632, -1568, -1760, -1696,
    -688, -656, -752, -720, -560, -528, -624, -592,
    -944, -912, -1008, -976, -816, -784, -880, -848,
    5504, 5248, 6016, 5760, 4480, 4224, 4992, 4736,
    7552, 7296, 8064, 7808, 6528, 6272, 7040, 6784,
    2752, 2624, 3008, 2880, 2240, 2112, 2496, 2368,
    3776, 3648, 4032, 3904, 3264, 3136, 3520, 3392,
    22016, 20992, 24064, 23040, 17920, 16896, 19968, 18944,
    30208, 29184, 32256, 31232, 26112, 25088, 28160, 27136,
    11008, 10496, 12032, 11520, 8960, 8448, 9984, 9472,
    15104, 14592, 16128, 15616, 13056, 12544, 14080, 13568,
    344, 328, 376, 360, 280, 264, 312, 296,
    472, 456, 504, 488, 408, 392, 440, 424,
    88, 72, 120, 104, 24, 8, 56, 40,
    216, 200, 248, 232, 152, 136, 184, 168,
    1376, 1312, 1504, 1440, 1120, 1056, 1248, 1184,
    1888, 1824, 2016, 1952, 1632, 1568, 1760, 1696,
    688, 656, 752, 720, 560, 528, 624, 592,
    944, 912, 1008, 976, 816, 784, 880, 848
  }; 
  
  public static short alaw2linear( byte ulawbyte) 
  { 
    return a2l[ulawbyte & 0xFF];
  } 
  
  public static byte linear2alaw(short pcm_val) 
    /* 2's complement (16-bit range) */
  {
    byte mask;
    byte seg=8;
    byte aval;
    
    if (pcm_val >= 0) {
      mask = (byte) 0xD5;  /* sign (7th) bit = 1 */
    } else {
      mask = 0x55;  /* sign bit = 0 */
      pcm_val = (short) (-pcm_val - 8);
    }
    
    /* Convert the scaled magnitude to segment number. */
    for (int i = 0; i < 8; i++) {
      if (pcm_val <= seg_end[i]) {
        seg=(byte) i;
        break;
      }
    }
    
    /* Combine the sign, segment, and quantization bits. */
    if (seg >= 8)  /* out of range, return maximum value. */
      return (byte) ((0x7F ^ mask) & 0xFF);
    else {
      aval = (byte) (seg << SEG_SHIFT);
      if (seg < 2)
        aval |= (pcm_val >> 4) & QUANT_MASK;
      else
        aval |= (pcm_val >> (seg + 3)) & QUANT_MASK;
      return (byte) ((aval ^ mask) & 0xFF);
    }
  }
  
  
  
  
  /**
   * Converts a 16 bit sample of type <code>int</code> to 2 bytes in an array.
   * <code>sample</code> is interpreted as signed (as Java does).
   * <p>
   * For little endian, buffer[byteOffset] is filled with low byte of sample, 
   * and buffer[byteOffset+1] is filled with high byte of sample + sign bit.
   * <p> For big endian, this is reversed.
   * <p> Before calling this function, it should be assured that 
   * <code>sample</code> is in the 16bit range - it will not be clipped.
   * <p> This is a reference function.
   */ 
  public static void intToBytes16( int sample, byte [] buffer, int byteOffset, 
                                   boolean bigEndian) 
  { 
    if (bigEndian) 
    {
      buffer[byteOffset++]=( byte ) (sample >> 8);
      buffer[byteOffset]=( byte ) (sample & 0xFF);
    } 
    else 
    {
      buffer[byteOffset++]=( byte ) (sample & 0xFF);
      buffer[byteOffset]=( byte ) (sample >> 8);
    }
  } 
  
  /**
   * Converts a 24 bit sample of type <code>int</code> to 3 bytes in an array.
   * <code>sample</code> is interpreted as signed (as Java does).
   * <p>
   * For little endian, buffer[byteOffset] is filled with low byte of sample, 
   * and buffer[byteOffset+2] is filled with the high byte of sample + 
   * sign bit.
   * <p> For big endian, this is reversed.
   * <p> Before calling this function, it should be assured that 
   * <code>sample</code> is in the 24bit range - it will not be clipped.
   * <p> This is a reference function.
   */ 
  public static void intToBytes24( int sample, byte [] buffer, 
                                   int byteOffset, boolean bigEndian) 
  { 
    if (bigEndian) 
    {
      buffer[byteOffset++]=( byte ) (sample >> 16);
      buffer[byteOffset++]=( byte ) ((sample >>> 8) & 0xFF);
      buffer[byteOffset]=( byte ) (sample & 0xFF);
    } 
    else 
    {
      buffer[byteOffset++]=( byte ) (sample & 0xFF);
      buffer[byteOffset++]=( byte ) ((sample >>> 8) & 0xFF);
      buffer[byteOffset]=( byte ) (sample >> 16);
    }
  } 
  
  /**
   * Converts a 32 bit sample of type <code>int</code> to 4 bytes in an array.
   * <code>sample</code> is interpreted as signed (as Java does).
   * <p>
   * For little endian, buffer[byteOffset] is filled with lowest byte of 
   * sample, and buffer[byteOffset+3] is filled with the high byte of 
   * sample + sign bit.
   * <p> For big endian, this is reversed.
   * <p> This is a reference function.
   */ 
  public static void intToBytes32( int sample, byte [] buffer, 
                                   int byteOffset, boolean bigEndian) 
  { 
    if (bigEndian) 
    {
      buffer[byteOffset++]=( byte ) (sample >> 24);
      buffer[byteOffset++]=( byte ) ((sample >>> 16) & 0xFF);
      buffer[byteOffset++]=( byte ) ((sample >>> 8) & 0xFF);
      buffer[byteOffset]=( byte ) (sample & 0xFF);
    } 
    else 
    {
      buffer[byteOffset++]=( byte ) (sample & 0xFF);
      buffer[byteOffset++]=( byte ) ((sample >>> 8) & 0xFF);
      buffer[byteOffset++]=( byte ) ((sample >>> 16) & 0xFF);
      buffer[byteOffset]=( byte ) (sample >> 24);
    }
  } 
  
  /*
   * Byte<->Int conversions for unsigned pcm data were written
   * by myself with help from Real's Java How-To:
   * http://www.rgagnon.com/javadetails/java-0026.html
   */
  
  public static int unsignedByteToInt(byte b) 
  {
    /* 
     * & 0xFF while seemingly doing nothing to the individual bits,
     * forces java to recognize the byte as unsigned.  so, we return to
     * the calling function a number between 0 and 256.
     */
    return ((int) b & 0xFF);
  }
  
  public static int unsignedByteToInt16(byte[] buffer, int offset, 
                                         boolean isBigEndian)
  {
    /*
     * here, we want to take the first byte and shift it left
     * 8 bits then concatenate on the 8 bits in the second byte.
     * now we have a 16 bit number that java will recognize as
     * unsigned, so we return a number in the range [0, 65536]
     */
    
    if(isBigEndian)
    {
      return ( (unsignedByteToInt(buffer[offset]) << 8) |
              unsignedByteToInt(buffer[offset+1]) );
    }
    else
    {
      return( (unsignedByteToInt(buffer[offset+1]) << 8) |
             unsignedByteToInt(buffer[offset]));
    }
    
  }
  
  public static int unsignedByteToInt24(byte[] buffer, int offset,
                                        boolean isBigEndian)
  {
    if(isBigEndian)
    {
      return ( (unsignedByteToInt(buffer[offset]) << 16) |
              (unsignedByteToInt(buffer[offset+1]) << 8) |
              unsignedByteToInt(buffer[offset+2]));
    }
    else
    {
      return ( (unsignedByteToInt(buffer[offset+2]) << 16) |
              (unsignedByteToInt(buffer[offset+1]) << 8) |
              unsignedByteToInt(buffer[offset]));
    }
  }
  
  public static int unsignedByteToInt32(byte[] buffer, int offset,
                                        boolean isBigEndian)
  {
    if(isBigEndian)
    {
      return( (unsignedByteToInt(buffer[offset]) << 24) |
             (unsignedByteToInt(buffer[offset+1]) << 16) |
             (unsignedByteToInt(buffer[offset+2]) << 8) |
             unsignedByteToInt(buffer[offset+3]) );
    }
    else
    {
      return((unsignedByteToInt(buffer[offset+3]) << 24) |
             (unsignedByteToInt(buffer[offset+2]) << 16) |
             (unsignedByteToInt(buffer[offset+1]) << 8) |
             unsignedByteToInt(buffer[offset]) );
    }
  }
  
  public static byte intToUnsignedByte(int sample)
  {
    /*
     * does the reverse of the function above
     * we have an integer that is signed, so we're in the range 
     * [-128, 127], we want to convert to an unsigned number in 
     * the range [0,256], then put that into an unsigned byte
     * all while java tries to treat everythign as signed.
     * 
     * so.... say we want to set the sample value to -128
     * in our unsigned byte, this translates to 0, so we want
     * java's representation of -128: 10000000 to instead be stored
     * as 0: 00000000 so, we simply xor with -128, flipping the sign bit
     *
     * another example we want to store the max value 127: 01111111
     * translating into the unsigned range, the max is 256: 11111111
     * again, you can see all we need to change is the sign bit.
     *
     * and lastly, for something in the middle:
     * say we want to store the value 0: 00000000
     * translating into the unsigned range, we have the middle
     * value 128: 10000000
     * again, we just want to flip the first bit
     *
     * something a little more tricky... say we want to store the value 32
     * now this translates to 32--128 = 160 in unsigned representation
     * so we start with 32 = 00100000 and we want to go to
     *                 160 = 10100000 
     *
     * see, we just flip the sign bit, its the same as adding 128 which
     * is how we translate between  [-128,127] and [0,256].
     */
    return((byte)(sample ^ -128));
  }
  
  
  
  public static void intToUnsignedBytes16(int sample, byte [] buffer, 
                                          int byteOffset, boolean bigEndian) 
  {
    
    /* 
     * for this comment only, treat ^ not as XOR as we use it in java
     * but as an exponent symbol like on a calculator, i thought 2^15 
     * would be clearer than 32768.
     * the theory here is very simmilar to the 8 bit conversion we
     * did above.  only now we have 16 bits we want to write into.
     * so, we're going from the range [-2^15, 2^15-1] into the range
     * [0, 2^16].  again, to translate, we just need to add 2^15 to
     * our number, so we get the first byte, by shifting right 8 bits, 
     * (note: >>> is unsigned shift), and then XOR with -128 to flip the
     * sign bit.  for the second byte, we just want the last 8 bits
     * of our integer, so we & with 0xff to tell java to treat this
     * as unsigned, and just copy over the bit values.
     */
    if(bigEndian)
    {
      buffer[byteOffset] = (byte)(sample >>> 8 ^ -128);
      buffer[byteOffset+1] = (byte)(sample & 0xff);
    }
    else
    {
      buffer[byteOffset+1] = (byte)(sample >>> 8 ^ -128);
      buffer[byteOffset] = (byte)(sample & 0xff);
    }
  }
  
  public static void intToUnsignedBytes24(int sample, byte [] buffer, 
                                          int byteOffset, boolean bigEndian)
  {
    if(bigEndian)
    {
      buffer[byteOffset] = (byte)(sample >>> 16 ^ -128);
      buffer[byteOffset+1] = (byte)(sample >>> 8);
      buffer[byteOffset +2] = (byte)(sample & 0xff);
    }
    else
    {
      buffer[byteOffset+2] = (byte)(sample >>> 16 ^ -128);
      buffer[byteOffset+1] = (byte)(sample >>> 8);
      buffer[byteOffset] = (byte)(sample & 0xff);
    }
  }
  
  public static void intToUnsignedBytes32(int sample, byte [] buffer, 
                                          int byteOffset, boolean bigEndian)
  {
    if(bigEndian)
    {
      buffer[byteOffset] = (byte)(sample >>> 24 ^ -128);
      buffer[byteOffset+1] = (byte)(sample >>> 16);
      buffer[byteOffset+2] = (byte)(sample >>> 8);
      buffer[byteOffset+3] = (byte)(sample & 0xff);
    }
    else
    {
      buffer[byteOffset+3] = (byte)(sample >>> 24 ^ -128);
      buffer[byteOffset+2] = (byte)(sample >>> 16);
      buffer[byteOffset+1] = (byte)(sample >>> 8);
      buffer[byteOffset] = (byte)(sample & 0xff);
    }
  }
}